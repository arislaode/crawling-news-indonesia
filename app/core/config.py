# app/core/config.py
from starlette.config import Config

config = Config(".env")

DB_HOST = config("DB_HOST", cast=str)
DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=str)
DB_NAME = config("DB_NAME", cast=str)
DB_PORT = config("DB_PORT", cast=str)

REDIS_HOST = config("REDIS_HOST", cast=str)
REDIS_PORT = config("REDIS_PORT", cast=str)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"