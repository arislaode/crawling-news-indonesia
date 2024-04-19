# app/core/handle_response.py
from fastapi.responses import JSONResponse
from fastapi import status

def json_success_response(data: dict, status_code: int = status.HTTP_200_OK):
    return JSONResponse(status_code=status_code, content={"data": data})

def json_error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    return JSONResponse(status_code=status_code, content={"error": message})

def detailed_json_response(status_code: int = status.HTTP_200_OK, message: str = "", data: list = None, total_items: int = 0, total_pages: int = 0, current_page: int = 0):
    content = {
        "status": "success" if status_code == status.HTTP_200_OK else "error",
        "message": message,
        "data": data,
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": current_page
    }
    return JSONResponse(status_code=status_code, content=content)