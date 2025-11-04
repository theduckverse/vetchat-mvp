# --- connectivity test (temporary) ---
import os, httpx
from fastapi import HTTPException

@app.get("/ping-openai")
async def ping_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing OPENAI_API_KEY")

    try:
        async with httpx.AsyncClient(timeout=10) as ac:
            r = await ac.get(
                "https://api.openai.com/v1/models",
                headers={"Authorization": f"Bearer {api_key}"},
            )
        return {"status": r.status_code, "ok": r.status_code < 400}
    except Exception as e:
        # log and surface the exact error type/message
        print("[PING OPENAI ERROR]", repr(e))
        raise HTTPException(status_code=502, detail=f"Ping failed: {e}")
