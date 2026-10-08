# Паттерн FACTORY: создаёт нужный класс билета по названию,
# скрывая детали создания от остального кода.

from models import EconomyTicket, BusinessTicket, FirstTicket


class TicketFactory:
    @staticmethod
    def create(class_name, ticket_id, passenger, base_price):
        if class_name == "эконом":
            return EconomyTicket(ticket_id, passenger, base_price)
        elif class_name == "бизнес":
            return BusinessTicket(ticket_id, passenger, base_price)
        elif class_name == "первый":
            return FirstTicket(ticket_id, passenger, base_price)
        else:
            raise ValueError("Неизвестный класс билета")
