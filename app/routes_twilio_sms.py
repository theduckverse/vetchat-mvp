
import os, base64, hmac, hashlib
from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_session
from .risk import is_crisis
from .llm import chat_once
from .store import start_or_get_conversation, save_message

router = APIRouter()

def validate_twilio_signature(url: str, params: dict, received_sig: str, auth_token: str) -> bool:
    # Twilio signature = base64( HMAC-SHA1( auth_token, url + concatenated_params ) )
    # params must be in lexicographic order by key
    s = url + ''.join([k + params[k] for k in sorted(params.keys())])
    digest = hmac.new(auth_token.encode(), s.encode(), hashlib.sha1).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(received_sig or "", expected)

@router.post("/twilio/inbound", response_class=PlainTextResponse)
async def inbound_sms(request: Request, session: AsyncSession = Depends(get_session)):
    form = await request.form()
    from_number = (form.get("From") or "").strip()
    body = (form.get("Body") or "").strip()

    if not from_number or not body:
        return " "

    # Optional: verify signature (recommended in prod)
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    sig = request.headers.get("X-Twilio-Signature")
    if auth_token and sig:
        try:
            valid = validate_twilio_signature(str(request.url), dict(form), sig, auth_token)
        except Exception:
            valid = False
        if not valid:
            # Fail quietly to avoid leaking details
            return " "

    conv = await start_or_get_conversation(session, channel="sms", user_ref=from_number)
    await save_message(session, conv.id, "user", body)

    crisis = is_crisis(body)
    ai = await chat_once(body, crisis=crisis)

    await save_message(session, conv.id, "assistant", ai, crisis_flag=crisis)
    await session.commit()

    crisis_footer = ("\n\nNeed help now? Veterans Crisis Line: Dial 988, then press 1. Or text 838255.") if crisis else ""
    # Return plain text for SMS
    return (ai[:1500] + crisis_footer)
