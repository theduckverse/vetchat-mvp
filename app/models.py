
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Text, Boolean, ForeignKey, Enum, DateTime, func
import enum
import uuid

class Base(DeclarativeBase):
    pass

class ChannelEnum(str, enum.Enum):
    sms = "sms"
    web = "web"

class RoleEnum(str, enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    channel: Mapped[ChannelEnum] = mapped_column(Enum(ChannelEnum), nullable=False)
    user_ref: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    crisis_flag: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

class Feedback(Base):
    __tablename__ = "feedback"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"))
    rating: Mapped[int] = mapped_column()
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
