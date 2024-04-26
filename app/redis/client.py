import redis
from app.core.config import REDIS_HOST, REDIS_PORT

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)