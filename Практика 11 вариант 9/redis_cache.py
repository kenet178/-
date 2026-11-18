import json
import os


class RedisFlightSearchCache:
    PREFIX = 'airline:search:'

    def __init__(self, client=None):
        self.client = client
        if self.client is None:
            try:
                import redis
                self.client = redis.Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
                                                   decode_responses=True, socket_connect_timeout=0.15,
                                                   socket_timeout=0.15)
            except ImportError:
                pass

    def _key(self, destination):
        return self.PREFIX + (destination or '*').strip().casefold()

    def get(self, destination):
        if self.client is None: return None
        try:
            value = self.client.get(self._key(destination))
            return json.loads(value) if value is not None else None
        except Exception: return None  

    def set(self, destination, value, ttl=60):
        if self.client is not None:
            try: self.client.set(self._key(destination), json.dumps(value, ensure_ascii=False), ex=ttl)
            except Exception: pass

    def invalidate_all(self):
        if self.client is not None:
            try:
                keys = list(self.client.scan_iter(self.PREFIX + '*'))
                if keys: self.client.delete(*keys)
            except Exception: pass
