# parsers/peradaban.py
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import dateparser
from app.crud import crud_news
import time


logger = setup_logger('peradaban_parser')

def fetch_html_peradaban(url, header):
    URL = f"https://www.{url}/category/berita/"
    response = requests.get(URL, headers=header)
    time.sleep(1)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content from peradaban.")
        return response.text
    else:
        logger.error(f"Error fetching the URL peradaban.id: HTTP {response.status_code}")
        return None

def extract_details_peradaban(article, sources):
    url_category = f"https://f{sources}/category/berita/"
    category = url_category.split("/")[4]
    
    date_selector = 'div > div > span:nth-of-type(2)'
    date_tag = article.select_one(date_selector)
    raw_date = date_tag.get_text(strip=True) if date_tag else None
    
    if raw_date:
        try:
            parsed_date = dateparser.parse(raw_date, date_formats=['%B %d, %Y'], locales=['en', 'id'])
            date = parsed_date.strftime('%d/%m/%Y')
        except Exception as e:
            date = "Date parsing peradaban error"
            logger.error(f"Failed to parse date: {raw_date}, Error: {str(e)}")
    else:
        date = "Tanggal peradaban tidak ditemukan"
        logger.error("Date tag not found.")

    return date, category, sources

def parse_and_save_to_db_peradaban(html, url, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.select('#posts-container > li.post-item')

    titles = []
    articles_data = []

    for article in articles:
        title_selector = 'div > h2'
        link_selector = 'div > a'
        thumbnail_selector = 'a > img'

        title_tag = article.select_one(title_selector)
        title = title_tag.get_text(strip=True) if title_tag else "Judul peradaban tidak ditemukan"

        link_tag = article.select_one(link_selector)
        link = link_tag['href'] if link_tag else "Link peradaban tidak ditemukan"

        img_tag = article.select_one(thumbnail_selector)
        thumbnail = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else "Thumbnail peradaban tidak ditemukan"

        date, category, source = extract_details_peradaban(article, url)
        
        titles.append(title)
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
        logger.info("Data from peradaban successfully saved to the database.")
    except Exception as e:
        db_session.rollback()
        logger.error(f"Failed to save data from peradaban to the database: {str(e)}")
