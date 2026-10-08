# Модели: билеты разных классов обслуживания

from enum import Enum


# Класс обслуживания (Enum)
class TicketClass(Enum):
    ECONOMY = "эконом"
    BUSINESS = "бизнес"
    FIRST = "первый"


# Базовый класс билета
class Ticket:
    def __init__(self, ticket_id, passenger, base_price):
        self.id = ticket_id
        self.passenger = passenger
        self.base_price = base_price          # базовая цена рейса
        self.ticket_class = TicketClass.ECONOMY
        self.multiplier = 1.0                 # множитель класса
        self.price = base_price               # итоговая цена (посчитается позже)

    def __str__(self):
        return (f"Билет {self.id} | {self.passenger} | "
                f"{self.ticket_class.value} | {self.price} руб")


# Эконом-класс
class EconomyTicket(Ticket):
    def __init__(self, ticket_id, passenger, base_price):
        super().__init__(ticket_id, passenger, base_price)
        self.ticket_class = TicketClass.ECONOMY
        self.multiplier = 1.0


# Бизнес-класс (дороже)
class BusinessTicket(Ticket):
    def __init__(self, ticket_id, passenger, base_price):
        super().__init__(ticket_id, passenger, base_price)
        self.ticket_class = TicketClass.BUSINESS
        self.multiplier = 2.0


# Первый класс (самый дорогой)
class FirstTicket(Ticket):
    def __init__(self, ticket_id, passenger, base_price):
        super().__init__(ticket_id, passenger, base_price)
        self.ticket_class = TicketClass.FIRST
        self.multiplier = 3.0
