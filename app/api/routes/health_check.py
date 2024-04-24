# app/api/routes/news.py
from fastapi import APIRouter, status
from app.core.handle_response import detailed_json_response

router = APIRouter()

@router.get("/healthz/")
def healthz():
    return detailed_json_response(
        status_code=status.HTTP_200_OK,
        message="Service up and running!"
    )