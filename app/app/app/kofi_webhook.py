# app/kofi_webhook.py
import os, hmac, hashlib, json
from fastapi import APIRouter, Header, HTTPException, Request
from .db import SessionLocal, Supporter

router = APIRouter()
SECRET = (os.getenv("KOFI_WEBHOOK_SECRET") or "").encode()

@router.post("/kofi/webhook")
async def kofi_webhook(request: Request, x_kofi_signature: str = Header(None)):
    # 1) Verify we have a secret configured
    if not SECRET:
        raise HTTPException(500, "Missing KOFI_WEBHOOK_SECRET")

    # 2) Read raw body (Ko-fi signs the raw JSON)
    raw = await request.body()

    # 3) Verify signature
    digest = hmac.new(SECRET, raw, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, x_kofi_signature or ""):
        raise HTTPException(401, "Invalid signature")

    # 4) Parse payload
    data = json.loads(raw.decode("utf-8"))
    event_type = (data.get("type") or "").lower()

    # Ko-fi may send email under different fields; prefer 'email'
    email = (data.get("email") or data.get("payer_email") or "").lower().strip()
    make_active = ("subscription" in event_type) or ("membership" in event_type) or ("renew" in event_type)
    make_inactive = ("cancel" in event_type) or ("refund" in event_type)

    # 5) If there is an email, upsert supporter status
    if email:
        db = SessionLocal()
        try:
            rec = db.get(Supporter, email)
            if not rec:
                rec = Supporter(email=email, active=True)
                db.add(rec)
            if make_active:
                rec.active = True
            if make_inactive:
                rec.active = False
            db.commit()
        finally:
            db.close()

    # 6) Always return OK so Ko-fi stops retrying
    return {"ok": True}
