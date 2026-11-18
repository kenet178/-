import sys
from seed import seed
from mongo_repository import MongoRepository
from redis_cache import RedisCache
from service import FlightService
from pymongo.errors import PyMongoError
from redis.exceptions import RedisError


def connect():
    repo=MongoRepository()
    repo.client.admin.command('ping')
    cache=RedisCache()
    cache.r.ping()
    return FlightService(repo,cache)


def demonstration(service):
    repo=service.repo;cache=service.cache
    print('=== Практика 13, вариант 9: Авиакомпания ===')
    for name,records in repo.queries().items():print('ЗАПРОС:',name,'НАЙДЕНО:',len(records))
    print('ПЕРВОЕ ЧТЕНИЕ:',service.get('SU101')[1])
    print('ПОВТОРНОЕ ЧТЕНИЕ:',service.get('SU101')[1])
    service.change('SU101',{'status':'boarding'})
    print('ПОСЛЕ ИЗМЕНЕНИЯ:',service.get('SU101')[1])
    print('ПОИСК:',len(service.search('Москва')))
    print('ИСТОРИЯ ПОИСКА:',cache.nearest())
    print('БЛИЖАЙШИЕ РЕЙСЫ И МЕСТА:', [(f['number'], f['departure'], f['seats']) for f in service.upcoming()])
    cache.demonstration()
    for count in (100, 1000, 10000):
        print('СРАВНЕНИЕ:', service.benchmark('SU101', repeats=count))


def menu(service):
    while True:
        print('\n1. Список рейсов   2. Рейс по номеру  3. Поиск  4. Создать рейс')
        print('5. Изменить статус  6. Удалить рейс  7. SQL-подобные выборки Mongo')
        print('8. Redis-операции  9. Benchmark  10. Ближайшие рейсы  0. Выход')
        cmd=input('Выбор: ').strip()
        try:
            if cmd=='0':return
            if cmd=='1':
                for f in service.repo.all(): print(f['number'],f['origin'],'→',f['destination'],f['status'])
            elif cmd=='2':
                print(service.get(input('Номер рейса: ').strip()))
            elif cmd=='3':
                print(service.search(input('Ключевое слово: ').strip()))
            elif cmd=='4':
                number=input('Номер: ').strip().upper()
                origin=input('Откуда: ').strip()
                destination=input('Куда: ').strip()
                departure=input('Отправление YYYY-MM-DDTHH:MM:SS: ').strip()
                seats=int(input('Свободных мест: '))
                if not number or not origin or not destination or seats<0 or origin==destination:
                    raise ValueError('Проверьте номер, маршрут и места')
                print('ID:',service.add({'number':number,'origin':origin,'destination':destination,
                    'departure':departure,'aircraft':{'model':'Airbus A320'},'passengers':[],
                    'seats':seats,'status':'scheduled'}))
            elif cmd=='5':print('Обновлено:',service.change(input('Номер рейса: ').strip(),{
                'status':input('Статус: ').strip()}))
            elif cmd=='6':print('Удалено:',service.delete(input('Номер рейса: ').strip()))
            elif cmd=='7':
                for name,rows in service.repo.queries().items():print(name,':',len(rows))
            elif cmd=='8':service.cache.demonstration()
            elif cmd=='9':print(service.benchmark(input('Номер рейса: ').strip()))
            elif cmd == '10':
                for flight in service.upcoming():
                    print(flight['number'], flight['departure'], 'мест:', flight['seats'])
            else: print('Неизвестная команда')
        except (PyMongoError,RedisError,ValueError,KeyError) as error:print('Ошибка:',error)


def main():
    try:
        seed()
        service=connect()
        if '--demo-real' in sys.argv:demonstration(service)
        else:menu(service)
    except (PyMongoError, RedisError, ConnectionError) as error:
        print('Сервис MongoDB или Redis недоступен:',error)
        print('Запустите MongoDB и Redis как локальные службы и повторите запуск.')

if __name__=='__main__': main()
