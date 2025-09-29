from __future__ import annotations
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
# Para SQLite, check_same_thread=False permite uso em threads do Uvicorn/Starlette
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db() -> None:
    # Import tardio para evitar ciclos
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
