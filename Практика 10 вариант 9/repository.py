# Слой хранения рейсов (в памяти)

from models import Flight


class FlightRepository:
    def __init__(self):
        self._flights = []
        self._next_id = 1

    def add(self, data):
        flight = Flight(
            self._next_id,
            data["number"],
            data["origin"],
            data["destination"],
            int(data["price"]),
            int(data["seats"]),
            int(data.get("available", data["seats"])),
        )
        self._next_id = self._next_id + 1
        self._flights.append(flight)
        return flight

    def all(self):
        return self._flights

    def get(self, flight_id):
        for f in self._flights:
            if f.id == flight_id:
                return f
        return None

    def remove(self, flight_id):
        f = self.get(flight_id)
        if f is None:
            return False
        self._flights.remove(f)
        return True
