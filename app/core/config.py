# app/core/config.py
from starlette.config import Config

config = Config(".env")

DB_HOST = config("DB_HOST", cast=str)
DB_USER = config("DB_USER", cast=str)
DB_PASSWORD = config("DB_PASSWORD", cast=str)
DB_NAME = config("DB_NAME", cast=str)
DB_PORT = config("DB_PORT", cast=str)
DB_DIALECT = config("DB_DIALECT", cast=str, default="mysql")

REDIS_HOST = config("REDIS_HOST", cast=str)
REDIS_PORT = config("REDIS_PORT", cast=str)

match DB_DIALECT:
    case "mysql":
        SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    case "postgresql":
        SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"