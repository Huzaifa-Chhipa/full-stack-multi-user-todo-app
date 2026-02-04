from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class RoleType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default="New Conversation", max_length=200)
    user_id: str = Field(index=True)


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)


class MessageBase(SQLModel):
    role: RoleType = Field(sa_column_kwargs={"default": RoleType.USER})
    content: str = Field(min_length=1, max_length=5000)
    conversation_id: int = Field(index=True)
    user_id: str = Field(index=True)


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRead(MessageBase):
    id: int
    created_at: datetime
    updated_at: datetime


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=5000)