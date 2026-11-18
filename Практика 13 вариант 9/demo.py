from datetime import datetime, timedelta
from memory_storage import MemoryMongoRepository, MemoryRedisCache
from service import FlightService


def main():
    print('=== ПРАКТИКА 13. ВАРИАНТ 9: АВИАРЕЙСЫ ===')
    service = FlightService(MemoryMongoRepository(), MemoryRedisCache())
    flight = {'number':'SU901','origin':'Москва','destination':'Казань',
              'departure':(datetime.now() + timedelta(days=1)).isoformat(timespec='seconds'), 'aircraft':{'model':'Airbus A320', 'capacity':180},
              'passengers':[{'name':'Иван Петров'}], 'seats':40, 'status':'scheduled'}
    print('CREATE:', service.add(flight))
    print('CACHE MISS:', service.get('SU901'))
    print('CACHE HIT:', service.get('SU901'))
    print('SEARCH:', service.search('Москва'))
    print('UPCOMING:', service.upcoming())
    print('UPDATE:', service.change('SU901', {'seats':39}))
    print('AFTER UPDATE (MISS):', service.get('SU901'))
    print('BENCHMARK:', service.benchmark('SU901', repeats=20))
    print('DELETE:', service.delete('SU901'))
    print('FINAL:', service.repo.all())
    print('Демонстрация завершена успешно.')

if __name__ == '__main__':main()
