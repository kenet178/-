# Модель ресурса REST API: рейс

from dataclasses import dataclass


@dataclass
class Flight:
    id: int
    number: str
    origin: str
    destination: str
    price: int
    seats: int           # всего мест
    available: int       # свободных мест

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "origin": self.origin,
            "destination": self.destination,
            "price": self.price,
            "seats": self.seats,
            "available": self.available,
        }
