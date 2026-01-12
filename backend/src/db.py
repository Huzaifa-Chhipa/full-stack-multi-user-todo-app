from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
from .models.user import User  # Import User model to include in metadata
from .models.task import Task  # Import Task model to include in metadata

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)

async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    """Get database session"""
    async with AsyncSession(engine) as session:
        yield session