from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.db.models.news import News
from app.core.logger import setup_logger
import dateparser
from app.crud import crud_news
import time


logger = setup_logger('nuonline_parser')

def fetch_html_nuonline(url, header):
    URL = f"https://{url}/indeks"
    response = requests.get(URL, headers=header)
    time.sleep(1)
    if response.status_code == 200:
        logger.info("Successfully fetched the HTML content for nuonline.")
        return response.text
    else:
        logger.error(f"Error fetching the URL nuonline: HTTP {response.status_code}")
        return None

def extract_details_nuonline(article, source):
    raw_date = article.select_one('.text-gray-400.dark\\:text-gray-300').get_text(strip=True)
    try:
        parsed_date = dateparser.parse(raw_date, languages=['id'])
        date = parsed_date.strftime('%d/%m/%Y') if parsed_date else "Date parsing failed"
    except Exception as e:
        date = "Tanggal nuonline tidak ditemukan"
        logger.error(f"Failed to parse date: {raw_date}, Error: {e}")

    category = article.select_one('.bg-green-500.text-white').get_text(strip=True) if article.select_one('.bg-green-500.text-white') else "Kategori nuonline tidak ditemukan"
    
    return date, category, source

def parse_and_save_to_db_nuonline(html, source, db_session: Session):
    soup = BeautifulSoup(html, 'html.parser')
    article_parent = soup.select_one('#scrollableWrapper > div > div.flex.flex-1.dark\\:bg-black-dark.xl\\:mx-auto.xl\\:max-w-9xl > div.flex-1.sm\\:mt-0 > main > div.mt-8.flex.w-full.sm\\:mt-4.md\\:mt-4.md\\:flex-col > div.flex.w-full.flex-1.flex-col > div.flex-1.bg-white.dark\\:bg-black-dark.mt-9')

    if article_parent:
        first_article = article_parent.select_one('.border-gray2.relative.cursor-pointer.border-b-2.border-dashed.pb-2.dark\\:border-gray-500.mt-3.first\\:mt-0')
        subsequent_articles = article_parent.select('.border-gray2.flex.w-full.border-b-2.border-dashed.pb-2.first\\:mt-0.last\\:border-none.dark\\:border-gray-500.mt-3')
        articles = [first_article] + [art for art in subsequent_articles if art != first_article]

        titles = []
        articles_data = []

        for idx, article in enumerate(articles):
            if idx == 0:
                link_url = f'https://www.{source}' + article.select_one('.h-full.w-full.max-h-32 > a')['href'] if article.select_one('.h-full.w-full.max-h-32 > a') else 'No link found'
            else:
                link_url = f'https://www.{source}' + article.select_one('div.flex-1 > a')['href'] if article.select_one('div.flex-1 > a') else 'No link found'
            title = article.select_one('h1, h2').get_text(strip=True) if article.select_one('h1, h2') else 'No title found'
            thumbnail = article.select_one('img')['src'] if article.select_one('img') else 'No image found'
            date, category, source = extract_details_nuonline(article, source)
            
            titles.append(title)
            articles_data.append({
                'title': title,
                'thumbnail': thumbnail,
                'link': link_url,
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
            logger.info("Data nuonline successfully saved to the database.")
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to save data nuonline to the database: {str(e)}")
    else:
        logger.error("Parent container article not found. Check the selector.")
