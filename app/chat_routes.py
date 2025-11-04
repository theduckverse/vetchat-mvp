
from fastapi import APIRouter
from pydantic import BaseModel
from .risk import is_crisis
from .llm import chat_once
from fastapi import APIRouter
from pydantic import BaseModel
from .risk import is_crisis
from .llm import chat_once

router = APIRouter()

# --- Keyword help routing ---
HELP_KEYWORDS = {
    "housing": "You mentioned housing. Veterans can get housing assistance here: https://www.va.gov/homeless/",
    "addiction": "If you're struggling with addiction, the VA offers confidential help: https://www.va.gov/substance-abuse/",
    "suicide": "⚠️ If you are in crisis, please call 988 (press 1) or text 838255 for immediate help.",
    "finances": "For financial assistance and veteran benefits, visit: https://www.va.gov/finance/ or contact your local VA office.",
}

def detect_resource_link(message: str):
    """Check if message contains any of our help keywords."""
    for keyword, reply in HELP_KEYWORDS.items():
        if keyword in message.lower():
            return reply
    return None


# --- Chat route ---
class ChatIn(BaseModel):
    conversation_id: str | None = None
    message: str


@router.post("/chat")
async def chat(inp: ChatIn):
    message = inp.message.strip()
    crisis = is_crisis(message)

    # Keyword routing check
    keyword_reply = detect_resource_link(message)
    if keyword_reply:
        return {"reply": keyword_reply, "crisis_banner": ("suicide" in message.lower())}

    # Otherwise, send to LLM
    reply = await chat_once(inp.message, crisis=crisis)
    return {"reply": reply, "crisis_banner": crisis}

router = APIRouter()

class ChatIn(BaseModel):
    conversation_id: str | None = None
    message: str

@router.post("/chat")
async def chat(inp: ChatIn):
    crisis = is_crisis(inp.message)
    reply = await chat_once(inp.message, crisis=crisis)
    return {"reply": reply, "crisis_banner": crisis}
