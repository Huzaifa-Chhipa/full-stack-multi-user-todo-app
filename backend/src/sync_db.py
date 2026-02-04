from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
from .models import *  # Import all models

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_db")

# Convert asyncpg URL to psycopg2 for sync operations if needed
if DATABASE_URL.startswith("postgresql+asyncpg"):
    # Replace with psycopg2 driver for sync operations
    DATABASE_URL_SYNC = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
    # If psycopg2 is not available, fall back to sqlite for testing
    try:
        import psycopg2
        DATABASE_URL = DATABASE_URL_SYNC
    except ImportError:
        # Use SQLite for testing if PostgreSQL drivers not available
        DATABASE_URL = "sqlite:///./todo_test.db"

# Create sync engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables_sync():
    """Create database tables synchronously"""
    SQLModel.metadata.create_all(bind=engine)

def get_sync_session():
    """Get synchronous database session"""
    with Session(engine) as session:
        yield session