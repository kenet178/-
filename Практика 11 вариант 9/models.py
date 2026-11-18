from dataclasses import dataclass, asdict

@dataclass
class Flight:
    id: int
    number: str
    origin_id: int
    destination_id: int
    aircraft_id: int
    departure: str
    price: float
    free_seats: int

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class Airport:
    id: int
    code: str
    city: str

@dataclass
class Passenger:
    id: int
    full_name: str
    email: str
