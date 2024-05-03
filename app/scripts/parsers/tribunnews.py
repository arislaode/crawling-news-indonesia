import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import dateparser

logger = setup_logger('tribunnews_parser')

def fetch_html_tribunnews(url, header):
    URL = f"https://www.{url}/populer?section=nasional&type=6h"
    response = requests.get(URL, headers=header)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content from tribunnews.")
        return response.text
    else:
        logger.error(f"Error fetching the URL tribunnews.com: HTTP {response.status_code}")
        return None

def extract_details_tribunnews(article, source):
    date_tag = article.select_one('time')
    sources = f"https://www.{source}/populer?section=nasional&type=6h"
    category = sources.split("section=")[1].split("&")[0]  # Correctly extracts 'nasional'
    if date_tag:
        raw_date = date_tag.text.strip()
        try:
            parsed_date = dateparser.parse(date_string=raw_date, languages=['id'])
            date = parsed_date.strftime('%d/%m/%Y')
        except ValueError:
            date = "Date not found"
            logger.error(f"Failed to parse date: {raw_date}")
    else:
        date = "Date not found"

    return date, category, source

def parse_and_save_to_db_tribunnews(html, source, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('.lsi.pt10.pb10 ul > li')

    for article in articles:
        link_url = article.select_one('h3 a')['href']
        title = article.select_one('h3 a').get_text(strip=True)
        thumbnail = article.select_one('.fl.mb5.mr10 a img')['src']

        date, category, sources = extract_details_tribunnews(article, source)
        
        # Create a new News instance and add it to the session
        news_item = News(title=title, thumbnail=thumbnail, link=link_url, date=date, category=category, source=sources)
        db_session.add(news_item)
    
    try:
        db_session.commit()
        logger.info("Data from tribunnews successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data from tribunnews to the database: {str(e)}")
