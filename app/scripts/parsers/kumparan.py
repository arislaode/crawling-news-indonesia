# parsers/kumparan.py
import requests
from bs4 import BeautifulSoup
import dateparser
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger

logger = setup_logger('kumparan_parser')

def fetch_html_kumparan(url, header):
    URL = f"https://{url}/trending"
    response = requests.get(URL, headers=header)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content from Kumparan.")
        return response.text
    else:
        logger.error(f"Error fetching the URL from Kumparan: HTTP {response.status_code}")
        return None

def extract_details_kumparan(article, source):
    title_tag = article.find('span', attrs={'data-qa-id': 'title'})
    title = title_tag.text.strip() if title_tag else "Title not found"

    date_element = article.find('span', attrs={'data-qa-id': 'card-footer-date'})
    raw_date = date_element.text.strip() if date_element else 'Date not found'
    parsed_date = dateparser.parse(date_string=raw_date, locales=['id'])
    date_kumparan = parsed_date.strftime('%d/%m/%Y') if parsed_date else 'Date parsing failed'

    thumbnail_element = article.find('noscript')
    thumbnail_url = thumbnail_element.find('img', class_='no-script')['src'] if thumbnail_element else 'Thumbnail not found'

    link_element = article.find('a', {'aria-label': 'news-card-label-link', 'draggable': 'true'})
    link_url = f"https://kumparan.com{link_element['href']}" if link_element else 'Link not found'

    category_tag = article.find('span', attrs={'data-qa-id': 'author-name'})
    category = category_tag.text.strip().replace('Kumparan', '').strip().capitalize() if category_tag else "Category not found"
    if category.startswith('Kumparan'):
        category = category[len('Kumparan'):].strip().capitalize()

    return title, date_kumparan, thumbnail_url, link_url, category, source

def parse_and_save_to_db_kumparan(html, source, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    news_items = soup.find_all('div', attrs={'data-qa-id': 'news-item'})

    for item in news_items:
        title, date_kumparan, thumbnail_url, link_url, category, source = extract_details_kumparan(item, source)
        
        # Create a new News instance and add it to the session
        news_item = News(title=title, thumbnail=thumbnail_url, link=link_url, date=date_kumparan, category=category, source=source)
        db_session.add(news_item)
    
    try:
        db_session.commit()
        logger.info("Data kumparan successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data kumparan to the database: {str(e)}")