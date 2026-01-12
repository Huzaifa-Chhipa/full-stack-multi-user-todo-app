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
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=72)  # Limit to 72 chars for bcrypt

    @property
    def hashed_password(self):
        # Truncate password to 72 bytes if needed to comply with bcrypt limitations
        password_bytes = self.password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes and decode back to string
            password_str = password_bytes[:72].decode('utf-8', errors='ignore')
        else:
            password_str = self.password
        return pwd_context.hash(password_str)

class UserLogin(SQLModel):
    username: str
    password: str

class UserPublic(UserBase):
    id: str