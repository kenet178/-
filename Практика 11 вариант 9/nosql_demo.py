from redis_cache import RedisFlightSearchCache

def main() -> None:
    cache = RedisFlightSearchCache()
    if cache.client is None:
        print('Установите redis: python -m pip install redis')
        return
    try:
        cache.client.ping()
        key = 'airline:demo:requests'
        print('SET:', cache.client.set('airline:demo:flight', 'SU101', ex=60))
        print('GET:', cache.client.get('airline:demo:flight'))
        print('INCR:', cache.client.incr(key))
        print('TTL:', cache.client.ttl('airline:demo:flight'))
        cache.client.delete('airline:demo:flight', key)
        print('DELETE:', cache.client.get('airline:demo:flight'))
    except Exception as error:
        print('Redis не запущен. Установите и запустите Redis локально:', error)

if __name__ == '__main__':
    main()
