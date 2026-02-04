from sqlmodel import SQLModel, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
from .models import *  # Import all models to include in metadata

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_db")

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

# Create sync engine for compatibility with existing tools
sync_engine = create_engine(DATABASE_URL.replace('asyncpg://', 'psycopg2://'), echo=True, pool_pre_ping=True, pool_recycle=300)

async def create_db_and_tables():
    """Create database tables"""
    async with async_engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():  # Keep the original name for backward compatibility
    """Get async database session (for backward compatibility)"""
    async with AsyncSession(async_engine) as session:
        yield session

async def get_async_session():
    """Get async database session"""
    async with AsyncSession(async_engine) as session:
        yield session

def get_sync_session():
    """Get synchronous database session"""
    with Session(sync_engine) as session:
        yield session