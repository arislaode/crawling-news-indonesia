import logging
from app.db.session import SessionLocal
from app.scripts.parsers.detik import fetch_html_detik, parse_and_save_to_db_detik
from app.scripts.parsers.peradaban import fetch_html_peradaban, parse_and_save_to_db_peradaban
from app.scripts.parsers.tempo import fetch_html_tempo, parse_and_save_to_db_tempo
from app.scripts.parsers.kompas import fetch_html_kompas, parse_and_save_to_db_kompas
from app.redis.client import redis_conn
from app.core.config import DETIK_URL, PERADABAN_URL, TEMPO_URL, KOMPAS_URL, HEADERS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl_detik(db):
    try:
        html_content_detik = fetch_html_detik(DETIK_URL, HEADERS)
        if html_content_detik:
            parse_and_save_to_db_detik(html_content_detik, DETIK_URL, db)
    except Exception as e:
        logging.error(f"An error occurred during the Detik crawl: {e}")

def crawl_peradaban(db):
    try:
        html_content_peradaban = fetch_html_peradaban(PERADABAN_URL, HEADERS)
        if html_content_peradaban:
            parse_and_save_to_db_peradaban(html_content_peradaban, PERADABAN_URL, db)
    except Exception as e:
        logging.error(f"An error occurred during the Peradaban crawl: {e}")

def crawl_tempo(db):
    try:
        html_content_tempo = fetch_html_tempo(TEMPO_URL, HEADERS)
        if html_content_tempo:
            parse_and_save_to_db_tempo(html_content_tempo, TEMPO_URL, db)
    except Exception as e:
        logging.error(f"An error occurred during the tempo crawl: {e}")

def crawl_kompas(db):
    try:
        html_content_kompas = fetch_html_kompas(KOMPAS_URL, HEADERS)
        if html_content_kompas:
            parse_and_save_to_db_kompas(html_content_kompas, KOMPAS_URL, db)
    except Exception as e:
        logging.error(f"An error occurred during the kompas crawl: {e}")

def run_crawler():
    try:
        with SessionLocal() as db:
            crawl_detik(db)
            crawl_peradaban(db)
            crawl_tempo(db)
            crawl_kompas(db)
            redis_conn.flushdb()
    except Exception as e:
        logging.error(f"An error occurred in the run_crawler function: {e}")
    finally:
        redis_conn.close()
        logging.info("Redis connection closed")

if __name__ == "__main__":
    run_crawler()
