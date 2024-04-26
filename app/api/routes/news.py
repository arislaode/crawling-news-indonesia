# app/api/routes/news.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import init_db
from app.core.handle_response import detailed_json_response
from app.crud.crud_news import get_news_items, get_total_news_count

router = APIRouter()

@router.get("/news/")
def read_news(filter: str = Query(None), offset: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(init_db)):
    try:
        total_count = get_total_news_count(db, source=filter)
        news_items = get_news_items(db, source=filter, skip=offset, limit=limit)
        total_pages = (total_count + limit - 1) // limit
        current_page = offset // limit + 1
        if news_items:
            return detailed_json_response(
                status_code=status.HTTP_200_OK,
                message="News retrieved successfully",
                data=news_items,
                total_items=total_count,
                total_pages=total_pages,
                current_page=current_page
            )
        else:
            return detailed_json_response(status_code=404, message="No news found")
    except Exception as e:
        return detailed_json_response(status_code=500, message=f"An unexpected error occurred: {str(e)}")