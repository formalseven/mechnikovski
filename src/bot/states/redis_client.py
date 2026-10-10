import redis.asyncio as redis
from dotenv import dotenv_values
import os

config = {
    **dotenv_values(),
    **os.environ
}
if not config.get("REDIS_URL"):
    raise Exception("Error | Redis url not found!")
redis_client = redis.from_url(config.get("REDIS_URL"), decode_responses=True)