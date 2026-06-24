import json
from utils.redis_manager import redis_client
import redis


def get_cache(key: str):
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
    except (redis.RedisError, json.JSONDecodeError):
        pass
    return None


def set_cache(key: str, value, expiry: int = 300):
    try:
        redis_client.set(key, json.dumps(value), ex=expiry)
    except redis.RedisError:
        pass


def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except redis.RedisError:
        pass