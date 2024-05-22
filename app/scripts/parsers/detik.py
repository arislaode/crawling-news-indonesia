# parsers/detik.py
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import dateparser
from app.crud import crud_news
import time


logger = setup_logger('detik_parser')

def fetch_html_detik(url, header):
    URL = f"https://www.{url}/terpopuler"
    response = requests.get(URL, headers=header)
    time.sleep(1)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content detik.")
        return response.text
    else:
        logger.error(f"Error fetching the URL detik.com : HTTP {response.status_code}")
        return None

def extract_details_detik(article, sources):
    
    date_tag = article.find('span', attrs={"d-time": True})
    if date_tag:
        raw_date = date_tag['title'].strip()
        try:
            parsed_date = dateparser.parse(date_string=raw_date, locales=['id'])
            date = parsed_date.strftime('%d/%m/%Y')
        except ValueError:
            date = "Tanggal detik tidak ditemukan"
            logger.error(f"Failed to parse date: {raw_date}")
    else:
        date = "Tanggal detik tidak ditemukan"
    
    category_tag = article.select_one('.media__date')
    category = category_tag.contents[0].strip().split('|')[0] if category_tag else "Kategori detik tidak ditemukan"
    
    return date, category, sources

def parse_and_save_to_db_detik(html, URL, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article')

    titles = []
    articles_data = []

    for article in articles:
        link_tag = article.find('a', class_='media__link')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            if "foto" in link or "properti" in link or link.startswith("https://inet.detik.com/consumer"):
                continue

        title_tag = article.find('h3', class_='media__title')
        title = title_tag.get_text(strip=True) if title_tag else "Judul detik tidak ditemukan"

        titles.append(title)
        img_tag = article.find('img')
        thumbnail = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "Thumbnail detik tidak ditemukan"
        date, category, source = extract_details_detik(article, URL)

        articles_data.append({
            'title': title,
            'thumbnail': thumbnail,
            'link': link,
            'date': date,
            'category': category,
            'source': source
        })
        time.sleep(1)

    if titles:
        existing_titles = crud_news.is_titles_exist(db_session, titles)
        new_articles = [article for article in articles_data if article['title'] not in existing_titles]
    else:
        new_articles = articles_data

    for article in new_articles:
        news_item = News(
            title=article['title'],
            thumbnail=article['thumbnail'],
            link=article['link'],
            date=article['date'],
            category=article['category'],
            source=article['source']
        )
        db_session.add(news_item)

    try:
        db_session.commit()
        logger.info("Data detik successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data detik to the database: {str(e)}")


