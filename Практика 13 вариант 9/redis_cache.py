import json
import redis
from config import REDIS_URL
class RedisCache:
    def __init__(self,client=None):
        self.r=client or redis.Redis.from_url(REDIS_URL,decode_responses=True)
    def get_flight(self,number):
        data=self.r.get('flight:'+number)
        return json.loads(data) if data else None
    def cache_flight(self,number,doc,ttl=60):
        self.r.set('flight:'+number,json.dumps(doc,ensure_ascii=False),ex=ttl)
    def invalidate(self, number):
        self.r.delete('flight:' + number, 'flight:upcoming')

    def upcoming(self, repository, from_date):
        key = 'flight:upcoming'
        cached = self.r.get(key)
        if cached is None:
            records = repository.upcoming(from_date)
            self.r.set(key, json.dumps(records, ensure_ascii=False), ex=30)
        else:
            records = json.loads(cached)
        return [flight for flight in records if flight['departure'] >= from_date]
    def record_search(self,query):
        p=self.r.pipeline()
        p.incr('search:count');p.lpush('search:recent',query);p.ltrim('search:recent',0,19)
        p.sadd('search:unique',query);p.hincrby('search:terms',query,1)
        p.execute()
    def nearest(self):return self.r.lrange('search:recent',0,9)
    def demonstration(self):
        r=self.r
        r.set('test:string','ok');print('1 SET:',r.get('test:string'))
        print('2 GET:',r.get('test:string'))
        print('3 EXPIRE:',r.expire('test:string',120))
        print('4 INCR:',r.incr('test:counter'))
        print('5 HSET:',r.hset('test:flight',mapping={'number':'SU001','status':'scheduled'}))
        print('6 HGETALL:',r.hgetall('test:flight'))
        print('7 LPUSH:',r.lpush('test:recent','SU001'))
        print('8 LRANGE:',r.lrange('test:recent',0,-1))
        print('9 SADD:',r.sadd('test:unique','SU001'))
        print('10 SMEMBERS:',r.smembers('test:unique'))
        print('11 TTL:',r.ttl('test:string'))
        print('12 DEL:',r.delete('test:string'))
