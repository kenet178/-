# Модель предметной области: билет

from dataclasses import dataclass


@dataclass
class Ticket:
    id: int
    event: str        # мероприятие
    seat: str         # место
    price: int        # цена
    status: str = "свободен"   # "свободен" или "продан"

    # превращаем объект в словарь для передачи по сети (JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "event": self.event,
            "seat": self.seat,
            "price": self.price,
            "status": self.status,
        }
