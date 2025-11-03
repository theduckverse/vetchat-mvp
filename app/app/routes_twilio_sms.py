/routes_twilio_sms.py
from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
import re
from app.chat import chat_once  # your existing function

router = APIRouter()

CRISIS_PATTERNS = re.compile(r'(suicid|kill myself|end it|hurt myself|take my life|self[-\s]?harm|overdose|i want to die|can\'t go on)', re.I)
FOOTER = " If you are in crisis: Dial 988, then press 1. Or text 838255."

@router.post("/twilio/inbound", response_class=PlainTextResponse)
async def sms_inbound(From: str = Form(""), To: str = Form(""), Body: str = Form("")):
    user_text = Body.strip() or "Hello"
    # crisis-first safety
    if CRISIS_PATTERNS.search(user_text):
        reply = ("I'm really glad you reached out. You are not alone." + FOOTER)
    else:
        # keep context per phone number; you can also use (From, To) pair if you have multiple numbers
        reply = await chat_once(user_text, conversation_id=From)
        reply = (reply or "I'm here. How can I help?") + FOOTER

    # Return TwiML to send the SMS back
    return f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply[:1500]}</Message></Response>'
