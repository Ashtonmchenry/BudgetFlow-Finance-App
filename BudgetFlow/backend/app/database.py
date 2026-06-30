# This file sets up SQLAlchemy and the database session system, connecting FastAPI to the SQLite database
# Defines the database URL, creates an engine, and sets up a session factory.
# Also defines a base class for models and a dependency function to get a database session for API endpoints.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()