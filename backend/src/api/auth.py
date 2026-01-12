"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer
from jose import jwt
import os
from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db import get_session
from ..models.user import User, UserCreate
from passlib.context import CryptContext
from ..auth.jwt import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password"""
    try:
        # Check if this is a bcrypt hash (doesn't contain ':')
        if ':' not in hashed_password:
            return pwd_context.verify(plain_password, hashed_password)
        else:
            # This is a fallback hash in format: hash:salt
            stored_hash, salt = hashed_password.split(':', 1)
            import hashlib
            computed_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
            return computed_hash == stored_hash
    except Exception:
        # Fallback in case of bcrypt backend issues
        return False

def get_password_hash(password: str) -> str:
    """Hash a password"""
    try:
        # Ensure password is not longer than 72 bytes for bcrypt
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes and decode back to string
            password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)
    except Exception as e:
        # Handle bcrypt backend issues
        import hashlib
        # Fallback to SHA-256 with salt (not recommended for production)
        import secrets
        salt = secrets.token_hex(16)
        return hashlib.sha256((password + salt).encode()).hexdigest() + ":" + salt

@router.post("/token")
async def login_for_access_token(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Query for user by username
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    user = result.scalars().first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(
    username: str = Form(..., min_length=3, max_length=50),
    password: str = Form(..., min_length=6, max_length=72),
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user
    """
    # Check if user already exists
    statement = select(User).where(User.username == username)
    result = await session.execute(statement)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    hashed_password = get_password_hash(password)
    db_user = User(
        username=username,
        hashed_password=hashed_password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return {"message": "User created successfully", "user_id": db_user.id}

# Add other auth endpoints as needed