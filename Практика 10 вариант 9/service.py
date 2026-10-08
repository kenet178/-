# Слой бизнес-логики над рейсами

from repository import FlightRepository


class FlightService:
    def __init__(self):
        self.repo = FlightRepository()
        # начальные данные
        self.repo.add({"number": "SU100", "origin": "Москва", "destination": "Сочи",
                       "price": 5000, "seats": 50, "available": 3})
        self.repo.add({"number": "SU200", "origin": "Москва", "destination": "Казань",
                       "price": 4000, "seats": 40, "available": 0})
        self.repo.add({"number": "SU300", "origin": "Санкт-Петербург", "destination": "Сочи",
                       "price": 6000, "seats": 60, "available": 10})

    # список рейсов с фильтрацией по городу вылета и сортировкой по цене
    def list_all(self, origin=None, sort=None):
        flights = [f.to_dict() for f in self.repo.all()]
        if origin is not None:
            flights = [f for f in flights if f["origin"] == origin]
        if sort == "price":
            flights = sorted(flights, key=lambda f: f["price"])
        return flights

    def get(self, flight_id):
        f = self.repo.get(flight_id)
        return f.to_dict() if f is not None else None

    def create(self, data):
        return self.repo.add(data).to_dict()

    def update(self, flight_id, data):
        f = self.repo.get(flight_id)
        if f is None:
            return None
        # обновляем только переданные поля
        if "price" in data:
            f.price = int(data["price"])
        if "available" in data:
            f.available = int(data["available"])
        if "destination" in data:
            f.destination = data["destination"]
        return f.to_dict()

    def delete(self, flight_id):
        return self.repo.remove(flight_id)

    # СПЕЦИАЛИЗИРОВАННАЯ ОПЕРАЦИЯ: доступные рейсы (есть свободные места)
    def available(self):
        return [f.to_dict() for f in self.repo.all() if f.available > 0]
