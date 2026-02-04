from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserBase(SQLModel):
    username: str = Field(unique=True, min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_-]+$')

class User(UserBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = Field(unique=True, min_length=3, max_length=50, regex=r'^[a-zA-Z0-9_-]+$')
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=100)

    @property
    def hashed_password(self):
        return pwd_context.hash(self.password)

class UserLogin(SQLModel):
    username: str
    password: str

class UserPublic(UserBase):
    id: str