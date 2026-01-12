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
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

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
    user = result.first()

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
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user
    """
    # Check if user already exists
    statement = select(User).where(User.username == user_data.username)
    result = await session.execute(statement)
    existing_user = result.first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return {"message": "User created successfully", "user_id": db_user.id}

# Add other auth endpoints as needed