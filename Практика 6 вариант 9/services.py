# Бизнес-логика авиакомпании

from models import FlightStatus
from protocols import Reportable
from decorators import log_call, measure_time, require_status


# Регистрация пассажира на рейс.
# Декоратор с параметром проверяет, что рейс в статусе "регистрация".
@require_status(FlightStatus.REGISTRATION)
def register_passenger(flight, passenger):
    if len(flight.passengers) >= flight.plane.capacity:
        raise ValueError("Мест нет: рейс заполнен")
    flight.passengers.append(passenger)


# Функция использует объект через тип Protocol (структурная типизация)
def print_report(item: Reportable):
    print(item.get_report_data())


# Интроспекция: анализ объекта во время выполнения
def inspect_object(obj):
    print("Тип:", type(obj))
    print("Класс:", obj.__class__.__name__)
    print("Атрибуты:", vars(obj))
    print("Методы:", [name for name in dir(obj) if not name.startswith("_")])


class AirlineService:
    def __init__(self):
        self.flights = []   # список рейсов

    @log_call
    def add_flight(self, flight):
        self.flights.append(flight)

    def find_flight(self, number):
        for flight in self.flights:
            if flight.number == number:
                return flight
        return None

    # Сменить статус рейса
    def set_status(self, number, status):
        flight = self.find_flight(number)
        if flight is None:
            return None
        flight.status = status
        return flight

    # Зарегистрировать пассажира (вызывает функцию с декоратором require_status)
    def register(self, number, passenger):
        flight = self.find_flight(number)
        if flight is None:
            return None
        register_passenger(flight, passenger)
        return flight

    # Загрузка рейса в процентах
    def load_factor(self, flight):
        if flight.plane.capacity == 0:
            return 0
        return len(flight.passengers) / flight.plane.capacity * 100

    # Самые загруженные направления (по числу пассажиров)
    @measure_time
    def busiest_destinations(self):
        counts = {}
        for flight in self.flights:
            counts[flight.destination] = counts.get(flight.destination, 0) + len(flight.passengers)
        # сортируем по убыванию количества пассажиров
        return sorted(counts.items(), key=lambda kv: kv[1], reverse=True)
