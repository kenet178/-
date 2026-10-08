# Модели предметной области: авиакомпания

from dataclasses import dataclass, field
from enum import Enum


# Статусы рейса (Enum)
class FlightStatus(Enum):
    PLANNED = "запланирован"
    REGISTRATION = "регистрация"
    DEPARTED = "вылетел"
    COMPLETED = "завершён"
    CANCELLED = "отменён"


# Базовый класс предметной области
@dataclass
class Entity:
    id: int
    name: str


# Специализированный класс: пассажир
@dataclass
class Passenger(Entity):
    passport: str = ""

    # метод для протокола Reportable
    def get_report_data(self) -> str:
        return f"Пассажир {self.name} (паспорт {self.passport})"


# Специализированный класс: самолёт
@dataclass
class Plane(Entity):
    capacity: int = 0

    def get_report_data(self) -> str:
        return f"Самолёт {self.name}, мест: {self.capacity}"


# Рейс: содержит самолёт и список пассажиров
@dataclass
class Flight:
    id: int
    number: str
    origin: str
    destination: str
    plane: Plane
    status: FlightStatus = FlightStatus.PLANNED
    passengers: list = field(default_factory=list)

    def get_report_data(self) -> str:
        return (f"Рейс {self.number} {self.origin}->{self.destination}, "
                f"{self.status.value}, пассажиров: {len(self.passengers)}")
