# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base_class import Base
from app.core.config import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
