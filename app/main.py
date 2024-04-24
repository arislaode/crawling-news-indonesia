from fastapi import FastAPI
from app.api.routes import news as news_router
from app.api.routes import health_check as health_check_router

app = FastAPI()

app.include_router(news_router.router, prefix="/api/v1")
app.include_router(health_check_router.router, prefix="/api/v1")