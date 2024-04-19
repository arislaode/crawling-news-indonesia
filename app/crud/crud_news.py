from sqlalchemy.orm import Session
from app.db.models.news import News

def get_news_items(db: Session, source: str = None, skip: int = 0, limit: int = 10):
    query = db.query(News)
    if source:
        query = query.filter(News.source == source)
    news_items = query.offset(skip).limit(limit).all()
    return news_items

def get_total_news_count(db: Session, source: str = None):
    query = db.query(News)
    if source:
        query = query.filter(News.source == source)
    total_count = query.count()
    return total_count
