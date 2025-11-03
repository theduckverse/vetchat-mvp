
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Conversation, Message, ChannelEnum, RoleEnum
from .security import hash_user_ref

async def start_or_get_conversation(session: AsyncSession, *, channel: str, user_ref: str | None):
    hashed = hash_user_ref(user_ref) if user_ref else None
    stmt = select(Conversation).where(Conversation.channel == channel, Conversation.user_ref == hashed)
    res = await session.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        conv = Conversation(channel=ChannelEnum(channel), user_ref=hashed)
        session.add(conv)
        await session.flush()
    return conv

async def save_message(session: AsyncSession, conversation_id: str, role: str, content: str, crisis_flag: bool=False):
    msg = Message(conversation_id=conversation_id, role=RoleEnum(role), content=content, crisis_flag=crisis_flag)
    session.add(msg)
    await session.flush()
    return msg
