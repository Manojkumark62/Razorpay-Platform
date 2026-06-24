import redis
from core.config import settings

try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
except Exception:
    redis_client = None


def set_cache(key: str, value: str, expire: int = 300):
    try:
        if redis_client:
            redis_client.set(key, value, ex=expire)
    except redis.RedisError:
        pass


def get_cache(key: str):
    try:
        if redis_client:
            return redis_client.get(key)
    except redis.RedisError:
        pass
    return None


def delete_cache(key: str):
    try:
        if redis_client:
            redis_client.delete(key)
    except redis.RedisError:
        pass