"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import jwt
import os
from typing import Optional
from datetime import datetime, timedelta
from ..auth import create_access_token

router = APIRouter()

# Using a simple authentication for demonstration
# In a real app, this would integrate with Better Auth or a proper user database

from fastapi import Form

@router.post("/token")
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # In a real app, you would verify the username/password against a database
    # For now, we'll just accept any non-empty username/password combination
    # and generate a token with the username as the user_id
    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# Add other auth endpoints as needed