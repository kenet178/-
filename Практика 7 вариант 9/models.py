# Модели предметной области

from dataclasses import dataclass
from enum import Enum


# Статусы билета (Enum)
class TicketStatus(Enum):
    BOOKED = "забронирован"
    PAID = "оплачен"
    REFUNDED = "возвращён"
    REGISTERED = "зарегистрирован"


# Рейс
@dataclass
class Flight:
    number: str
    origin: str
    destination: str
    price: int
    seats: int


# Билет
@dataclass
class Ticket:
    id: int
    flight_number: str
    passenger: str
    status: TicketStatus = TicketStatus.BOOKED
