from fastapi import FastAPI

# use package-relative imports
from .routes_twilio_sms import router as sms_router
from .chat_routes import router as chat_router
from .metrics_routes import router as metrics_router
from .waitlist_routes import router as waitlist_router

app = FastAPI()

# mount routers
app.include_router(sms_router, prefix="/twilio", tags=["sms"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
app.include_router(waitlist_router, prefix="/waitlist", tags=["waitlist"])

@app.get("/")
def health():
    return {"message": "Vetchat (WatchMy6) is running"}

