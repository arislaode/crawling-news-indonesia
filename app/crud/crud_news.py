from sqlalchemy.orm import Session
from app.db.models.news import News
from app.redis.client import redis_conn
import json

def get_news_items(db: Session, source: str = None, skip: int = 0, limit: int = 10):
    redis_key = f"news:{source}:{skip}:{limit}"
    if redis_conn.exists(redis_key):
        redis_result = redis_conn.get(redis_key)
        news = json.loads(redis_result)
        return news

    query = db.query(News)
    if source:
        query = query.filter(News.source == source)
    news_items = query.offset(skip).limit(limit).all()
    news = [item.to_dict() for item in news_items]
    redis_conn.set(redis_key, json.dumps(news))
    return news

def get_total_news_count(db: Session, source: str = None):
    redis_key = f"news:{source}:count"
    if redis_conn.exists(redis_key):
        total_count = redis_conn.get(redis_key)
        return int(total_count)

    query = db.query(News)
    if source:
        query = query.filter(News.source == source)
    total_count = query.count()
    redis_conn.set(redis_key, total_count)
    return total_count

def delete_news(db: Session, start_date: str, end_date: str):
    db.query(News).filter(News.date >= start_date, News.date <= end_date).delete()
    db.commit()