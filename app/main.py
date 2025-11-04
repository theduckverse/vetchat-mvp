# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

from .chat_routes import router as chat_router
from .routes_twilio_sms import router as sms_router  # if you have it
from .metrics_routes import router as metrics_router  # if you have it
from .waitlist_routes import router as waitlist_router  # if you have it

app = FastAPI()

# (optional) CORS – generally fine for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"message": "Vetchat (WatchMy6) is running"}

# ---- connectivity test (temporary) ----
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
        print("[PING OPENAI ERROR]", repr(e))
        raise HTTPException(status_code=502, detail=f"Ping failed: {e}")

# ---- mount your routers ----
app.include_router(chat_router, prefix="/chat", tags=["chat"])
# app.include_router(sms_router, prefix="/twilio", tags=["sms"])
# app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
# app.include_router(waitlist_router, prefix="/waitlist", tags=["waitlist"])
