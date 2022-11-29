import redis
from setting import REDIS_URI

pool = redis.ConnectionPool(host=REDIS_URI, port=6379, db=5, decode_responses=True)
r = redis.Redis(connection_pool=pool, encoding_errors='ignore', socket_connect_timeout=1, retry_on_timeout=True)
