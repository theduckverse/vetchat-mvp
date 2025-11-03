
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .sms_routes import router as sms_router
from .chat_routes import router as chat_router
from .waitlist_routes import router as waitlist_router
from .metrics_routes import router as metrics_router

app = FastAPI(title="AI for Veterans (MVP)")

import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=float(os.getenv("SENTRY_TRACES", "0.1")))
    app.add_middleware(SentryAsgiMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW","*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sms_router)
app.include_router(chat_router)
app.include_router(waitlist_router)
app.include_router(metrics_router)

@app.get("/healthz")
async def healthz():
    return {"ok": True}
