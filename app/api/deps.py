from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def handle_error(status_code: int, message: str):
    raise HTTPException(status_code=status_code, detail=message)
