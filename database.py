from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
# Use DATABASE_URL env var if available (for production), else fallback to local
# Note: Render/Neon sometimes provide postgres:// which needs to be postgresql:// for SQLAlchemy
db_url = os.getenv("DATABASE_URL", "postgresql://postgres:Aa2282000%40@localhost:5432/inventory")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
engine=create_engine(db_url)
session=sessionmaker(autoflush=False,autocommit=False,bind=engine)

