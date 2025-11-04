# app/kofi_webhook.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from urllib.parse import parse_qs
import json

router = APIRouter()

@router.post("/kofi-webhook")
async def kofi_webhook(request: Request):
    """Handle Ko-fi payment notifications (JSON or form data)"""
    try:
        # Try JSON first
        try:
            data = await request.json()
        except:
            raw_body = await request.body()
            data = parse_qs(raw_body.decode())
            # Ko-fi wraps its real payload in a "data" key
            if "data" in data:
                data = json.loads(data["data"][0])

        print("✅ Ko-fi webhook received:", json.dumps(data, indent=2))

        # Extract supporter info
        supporter = {
            "name": data.get("from_name"),
            "email": data.get("email"),
            "amount": data.get("amount"),
            "type": data.get("type"),
            "message": data.get("message"),
        }

        print("🎉 Supporter:", supporter)

        # TODO: save to a supporters database here (e.g. SQLite, Supabase)
        # Example:
        # save_supporter_to_db(supporter)

        return JSONResponse({"status": "ok", "supporter": supporter})
    except Exception as e:
        print("❌ Ko-fi webhook error:", e)
        return JSONResponse({"status": "error", "message": str(e)}, status_code=400)



