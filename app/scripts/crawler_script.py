
from app.db.session import SessionLocal
from app.scripts.parsers.detik import fetch_html, parse_and_save_to_db, URL

def run_crawler():
    db = SessionLocal()
    try:
        html_content = fetch_html(URL)
        if html_content:
            parse_and_save_to_db(html_content, db)
    finally:
        db.close()

if __name__ == "__main__":
    run_crawler()