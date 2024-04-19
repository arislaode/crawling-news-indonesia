# parsers/detik.py
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import datetime
from dateutil import parser


logger = setup_logger('detik_parser')

URL = "https://www.detik.com/terpopuler"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def fetch_html(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content.")
        return response.text
    else:
        logger.error(f"Error fetching the URL: HTTP {response.status_code}")
        return None

def extract_details(article):
    source = "detik.com"
    
    date_tag = article.find('span', attrs={"d-time": True})
    if date_tag:
        raw_date = date_tag['title'].strip()
        raw_date = raw_date.replace('WIB', '').split(',', 1)[1].strip()
        try:
            parsed_date = parser.parse(raw_date)
            date = parsed_date.strftime('%d/%m/%Y')
        except ValueError:
            date = "Tanggal tidak ditemukan"
            logger.error(f"Failed to parse date: {raw_date}")
    else:
        date = "Tanggal tidak ditemukan"
    
    category_tag = article.select_one('.media__date')
    category = category_tag.contents[0].strip().split('|')[0] if category_tag else "Kategori tidak ditemukan"
    
    return date, category, source

def parse_and_save_to_db(html, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')

    for article in articles:
        link_tag = article.find('a', class_='media__link')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            if "foto" in link or "properti" in link or link.startswith("https://inet.detik.com/consumer"):
                continue

        title_tag = article.find('h3', class_='media__title')
        title = title_tag.get_text(strip=True) if title_tag else "Judul tidak ditemukan"

        img_tag = article.find('img')
        thumbnail = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "Thumbnail tidak ditemukan"

        date, category, source = extract_details(article)
        
        # Create a new News instance and add it to the session
        news_item = News(title=title, thumbnail=thumbnail, link=link, date=date, category=category, source=source)
        db_session.add(news_item)
    
    try:
        db_session.commit()
        logger.info("Data successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data to the database: {str(e)}")

