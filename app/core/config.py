# app/core/config.py
from starlette.config import Config

config = Config(".env")

DB_HOST = config("DB_HOST", cast=str)
DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=str)
DB_NAME = config("DB_NAME", cast=str)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"