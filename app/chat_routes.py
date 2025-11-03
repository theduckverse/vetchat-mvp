
from fastapi import APIRouter
from pydantic import BaseModel
from .risk import is_crisis
from .llm import chat_once

router = APIRouter()

class ChatIn(BaseModel):
    conversation_id: str | None = None
    message: str

@router.post("/chat")
async def chat(inp: ChatIn):
    crisis = is_crisis(inp.message)
    reply = await chat_once(inp.message, crisis=crisis)
    return {"reply": reply, "crisis_banner": crisis}
