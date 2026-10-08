# Слой хранения данных (репозитории).
# ISP/DIP: сервис работает через абстракцию Repository, не зная деталей хранения.

from abc import ABC, abstractmethod


# Абстрактный репозиторий (интерфейс)
class Repository(ABC):
    @abstractmethod
    def add(self, item):
        ...

    @abstractmethod
    def all(self):
        ...


# Репозиторий рейсов
class FlightRepository(Repository):
    def __init__(self):
        self._flights = []

    def add(self, flight):
        self._flights.append(flight)

    def all(self):
        return self._flights

    def get(self, number):
        for f in self._flights:
            if f.number == number:
                return f
        return None


# Репозиторий билетов
class TicketRepository(Repository):
    def __init__(self):
        self._tickets = []
        self._next_id = 1

    def add(self, ticket):
        self._tickets.append(ticket)

    def all(self):
        return self._tickets

    def get(self, ticket_id):
        for t in self._tickets:
            if t.id == ticket_id:
                return t
        return None

    def next_id(self):
        i = self._next_id
        self._next_id = self._next_id + 1
        return i
