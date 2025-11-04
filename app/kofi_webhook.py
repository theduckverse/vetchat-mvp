# app/kofi_webhook.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from urllib.parse import parse_qs

router = APIRouter()

@router.post("/kofi-webhook")
async def kofi_webhook(request: Request):
    """Handle Ko-fi payment notifications (JSON or form-encoded)"""
    try:
        # Try JSON first
        try:
            data = await request.json()
        except:
            # Fallback: Ko-fi often sends as form data
            raw_body = await request.body()
            data = parse_qs(raw_body.decode())

        print("✅ Ko-fi webhook received:", data)
        return JSONResponse({"status": "ok", "received": data})
    except Exception as e:
        print("❌ Ko-fi webhook error:", e)
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)


