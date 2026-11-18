from contextlib import closing
import tempfile
from pathlib import Path
from database import connect, initialize
from repository import FlightRepository
from service import AirlineService, BookingError


def main():
    print('=== ПРАКТИКА 11. ВАРИАНТ 9: АВИАКОМПАНИЯ ===')
    with tempfile.TemporaryDirectory() as folder:
        with closing(connect(str(Path(folder) / 'demo.db'))) as db:
            initialize(db)
            repo = FlightRepository(db)
            print('Рейсов:', len(repo.all()))
            print('ПОИСК:', repo.all('Казань')[:2])
            print('СТАТИСТИКА:', repo.stats()[:2])
            flight = repo.create('SU999', 1, 2, 1, '2026-12-29T11:00', 9500, 2)
            print('CREATE:', flight)
            print('UPDATE:', repo.update_price(flight['id'], 9200))
            ticket = AirlineService(db).book(flight['id'], 1, '1A')
            print('ТРАНЗАКЦИЯ (билет):', ticket)
            try:
                AirlineService(db).book(flight['id'], 2, '1A')
            except BookingError as error:
                print('КОНФЛИКТ МЕСТ:', error)
            print('ОСТАТОК МЕСТ:', repo.get(flight['id'])['free_seats'])
            print('ИТОГО ЗАПИСЕЙ:', len(repo.all()))
    print('Успешно. Дополнительные части: nosql_demo.py, origin_server.py, cdn_server.py.')

if __name__ == '__main__':main()
