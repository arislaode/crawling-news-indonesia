
from app.db.session import SessionLocal
from app.scripts.parsers.detik import fetch_html, parse_and_save_to_db, URL
from app.redis.client import redis_conn

def run_crawler():
    db = SessionLocal()
    try:
        html_content = fetch_html(URL)
        if html_content:
            parse_and_save_to_db(html_content, db)
            redis_conn.flushdb()
    finally:
        db.close()
        redis_conn.close()

if __name__ == "__main__":
    run_crawler()