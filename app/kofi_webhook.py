# app/kofi_webhook.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/kofi-webhook")
async def kofi_webhook(request: Request):
    """Handle Ko-fi payment notifications"""
    try:
        data = await request.json()
        print("Ko-fi webhook data:", data)
        return JSONResponse({"status": "ok", "received": data})
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)
