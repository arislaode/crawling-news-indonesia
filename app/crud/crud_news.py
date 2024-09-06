from sqlalchemy.orm import Session
from app.db.models.news import News
from app.redis.client import redis_conn
import json
import random
from app.core.config import DETIK_URL, TEMPO_URL, KOMPAS_URL, KUMPARAN_URL, TRIBUNNEWS_URL, NUONLINE_URL, PERADABAN_URL


def get_news_items(db: Session, source: str = None, skip: int = 0, limit: int = 10):
    redis_key = f"news:{source if source else 'all'}:{skip}:{limit}:random"

    if redis_conn.exists(redis_key):
        redis_result = redis_conn.get(redis_key)
        news = json.loads(redis_result)
        return news

    sources = [DETIK_URL, TEMPO_URL, KOMPAS_URL, KUMPARAN_URL, TRIBUNNEWS_URL, NUONLINE_URL, PERADABAN_URL]
    if source:
        sources = [source]

    all_news_items = []
    news_per_source = {}
    
    for src in sources:
        query = db.query(News).filter(News.source == src).order_by(News.id.desc())
        src_news_items = query.limit(2).all()
        if src_news_items:
            news_per_source[src] = src_news_items
            all_news_items.append(src_news_items[0])

    additional_news_items = []
    while len(additional_news_items) < 3:
        for src, items in news_per_source.items():
            if len(items) > 1 and items[1] not in additional_news_items:
                additional_news_items.append(items[1])
                if len(additional_news_items) == 3:
                    break

    all_news_items.extend(additional_news_items)

    random.shuffle(all_news_items)
    all_news_items = all_news_items[:limit]

    news = [item.to_dict() for item in all_news_items]

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

def is_titles_exist(db: Session, titles: list) -> set:
    existing_titles = db.query(News.title).filter(News.title.in_(titles)).all()
    return set(title[0] for title in existing_titles)
