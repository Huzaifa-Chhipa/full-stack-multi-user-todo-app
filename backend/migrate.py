"""
Database migration script for Todo Application
"""
import asyncio
import os
from src.db import create_db_and_tables

async def run_migrations():
    """Run database migrations to create tables"""
    print("Running database migrations...")
    await create_db_and_tables()
    print("Database migrations completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_migrations())