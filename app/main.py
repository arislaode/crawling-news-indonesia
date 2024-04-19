from fastapi import FastAPI
from app.api.routes import news as news_router

app = FastAPI()

app.include_router(news_router.router)