from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.session import init_db
from app.core.handle_response import detailed_json_response
from app.crud.crud_news import get_news_items, get_total_news_count
from urllib.parse import urlencode

router = APIRouter()

@router.get("/news/")
def read_news(filter: str = Query(None), offset: int = Query(0, ge=0), limit: int = Query(10, gt=0), db: Session = Depends(init_db)):
    try:
        total_count = get_total_news_count(db, source=filter)
        news_items = get_news_items(db, source=filter, skip=offset, limit=limit)
        total_pages = (total_count + limit - 1) // limit
        current_page = offset // limit + 1
        
        next_offset = offset + limit if offset + limit < total_count else None
        prev_offset = offset - limit if offset - limit >= 0 else None
        
        base_url = "/news/"
        next_url = None
        prev_url = None
        
        if next_offset is not None:
            next_url_params = {"filter": filter, "offset": next_offset, "limit": limit}
            next_url = f"{base_url}?{urlencode(next_url_params)}"
        
        if prev_offset is not None:
            prev_url_params = {"filter": filter, "offset": prev_offset, "limit": limit}
            prev_url = f"{base_url}?{urlencode(prev_url_params)}"
        
        if news_items:
            return detailed_json_response(
                status_code=status.HTTP_200_OK,
                message="News retrieved successfully",
                data=news_items,
                total_items=total_count,
                total_pages=total_pages,
                current_page=current_page,
                next_page=next_url,
                prev_page=prev_url
            )
        else:
            return detailed_json_response(status_code=404, message="No news found")
            
    except Exception as e:
        return detailed_json_response(status_code=500, message=f"An unexpected error occurred: {str(e)}")
