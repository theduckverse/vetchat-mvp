
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from .db import get_session

router = APIRouter()

@router.get("/metrics")
async def metrics(session: AsyncSession = Depends(get_session)):
    q_conv = await session.execute(text("SELECT COUNT(*) FROM conversations"))
    q_msg = await session.execute(text("SELECT COUNT(*) FROM messages"))
    q_crisis = await session.execute(text("SELECT COUNT(*) FROM messages WHERE crisis_flag = 1"))
    convs = q_conv.scalar() or 0
    msgs = q_msg.scalar() or 0
    crisis = q_crisis.scalar() or 0
    return {
        "conversations": convs,
        "messages": msgs,
        "messages_with_crisis_flag": crisis
    }
