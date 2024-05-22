from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import dateparser
from app.crud import crud_news
import time


logger = setup_logger('kompas_parser')

def fetch_html_kompas(url, header):
    URL = f"https://indeks.{url}/terpopuler"
    response = requests.get(URL, headers=header)
    time.sleep(1)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content for kompas.")
        return response.text
    else:
        logger.error(f"Error fetching the URL kompas.com : HTTP {response.status_code}")
        return None

def extract_details_kompas(article, source):
    date_tag = article.find('div', class_='articlePost-date')
    if date_tag:
        raw_date = date_tag.text.strip()
        try:
            parsed_date = dateparser.parse(date_string=raw_date, locales=['id'])
            date = parsed_date.strftime('%d/%m/%Y')
        except ValueError:
            date = "Tanggal kompas tidak ditemukan"
            logger.error(f"Failed to parse date: {raw_date}")
    else:
        date = "Tanggal kompas tidak ditemukan"

    category_tag = article.find('div', class_='articlePost-subtitle')
    category = category_tag.text.strip().capitalize() if category_tag else "Kategori kompas tidak ditemukan"
    
    return date, category, source

def parse_and_save_to_db_kompas(html, source, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('div', class_='articleItem')

    titles = []
    articles_data = []

    for article in articles:
        link_tag = article.find('a', class_='article-link')
        link = link_tag['href'] if link_tag else "Link kompas tidak ditemukan"
        
        title_tag = article.find('h2', class_='articleTitle')
        title = title_tag.text.strip() if title_tag else "Judul kompas tidak ditemukan"
        
        titles.append(title)
        img_tag = article.find('img')
        thumbnail = img_tag['src'] if img_tag else "Thumbnail kompas tidak ditemukan"

        date, category, source = extract_details_kompas(article, source)

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
        logger.info("Data kompas successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data kompas to the database: {str(e)}")
