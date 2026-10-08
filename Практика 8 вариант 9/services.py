# Сервис бронирования: объединяет три паттерна.
# Наследуется от BookingSubject (Observer), использует Factory и Strategy.

from factory import TicketFactory
from strategies import StandardPricing
from observers import BookingSubject


class BookingService(BookingSubject):
    def __init__(self, capacity=10):
        super().__init__()          # инициализация списка наблюдателей
        self.tickets = []
        self._next_id = 1
        self.capacity = capacity
        self.strategy = StandardPricing()   # стратегия по умолчанию

    # Сменить стратегию ценообразования (Strategy)
    def set_strategy(self, strategy):
        self.strategy = strategy

    # Забронировать билет
    def book(self, class_name, passenger, base_price):
        # FACTORY: создаём билет нужного класса
        ticket = TicketFactory.create(class_name, self._next_id, passenger, base_price)
        self._next_id = self._next_id + 1

        # цена = базовая * множитель класса * стратегия
        class_price = ticket.base_price * ticket.multiplier
        ticket.price = round(self.strategy.calculate(class_price))

        self.tickets.append(ticket)

        # OBSERVER: оповещаем всех подписчиков
        self.notify(f"Забронирован {ticket.ticket_class.value} билет {ticket.id} "
                    f"для {passenger}: {ticket.price} руб")
        return ticket
