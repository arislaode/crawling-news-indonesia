
from app.db.session import SessionLocal
from app.crud.crud_news import delete_news
from app.redis.client import redis_conn
from datetime import datetime, timedelta

def run_news_cleanup():
    db = SessionLocal()
    try:
        retention_from_today = 7
        end_date = datetime.today() - timedelta(days=retention_from_today)
        delete_news(db, "01/04/2024", end_date.strftime("%d/%m/%Y"))
        redis_conn.flushdb()
    finally:
        db.close()
        redis_conn.close()

if __name__ == "__main__":
    run_news_cleanup()