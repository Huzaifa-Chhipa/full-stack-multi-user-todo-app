import os
import sys
from pathlib import Path

# Add the backend/src directory to the path so we can import our models
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir / "src"))

from alembic import command
from alembic.config import Config

# Initialize alembic config
alembic_cfg = Config()
alembic_cfg.set_main_option("script_location", "alembic")
alembic_cfg.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "postgresql+asyncpg://neondb_owner:npg_GJ3iFQbqIM1j@ep-bitter-dawn-ahsp9gv7-pooler.c-3.us-east-1.aws.neon.tech/neondb"))

# Generate the initial migration
command.revision(alembic_cfg, autogenerate=True, message="Initial migration for Todo AI Chatbot")