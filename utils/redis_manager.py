import redis  # type: ignore[import]
from core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
)


def set_value(key: str, value: str, expiry: int = 300):
    try:
        redis_client.set(key, value, ex=expiry)
    except redis.RedisError:
        pass  # Gracefully degrade if Redis is unavailable


def get_value(key: str):
    try:
        return redis_client.get(key)
    except redis.RedisError:
        return None


def delete_value(key: str):
    try:
        redis_client.delete(key)
    except redis.RedisError:
        pass