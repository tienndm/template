from sqlite3 import DatabaseError
from bson import encode
from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import ConnectionError as RedisConnectionError

from .. import DATABASE_URI
from .base import hasReinitialize, normalizeUri

CHUNK_SIZE = 5000

asyncRedis = AsyncRedis.from_url(
    normalizeUri(DATABASE_URI),
    encoding='utf-8',
    decode_response=True,
    retry_on_error=[RedisConnectionError]
)

async def initializeRedis():
    if hasReinitialize(DATABASE_URI):
        async with asyncRedis.client() as client:
            cursor = '0'
            while cursor != 0:
                cursor, keys = await client.scan(cursor=int(cursor), match="*", count=CHUNK_SIZE)
                if keys:
                    await client.delete(*keys)

def getAsyncRedisClient() -> AsyncRedis:
    return asyncRedis.client()