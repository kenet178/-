# Сервисный слой (бизнес-логика).
# DIP: сервис зависит от абстракций (repository, payment, notifier),
# которые передаются через конструктор (Dependency Injection),
# а не создаёт конкретные классы сам.

from models import Ticket, TicketStatus


class BookingService:
    def __init__(self, flight_repo, ticket_repo, payment, notifier):
        self.flight_repo = flight_repo   # репозиторий рейсов
        self.ticket_repo = ticket_repo   # репозиторий билетов
        self.payment = payment           # обработчик оплаты
        self.notifier = notifier         # отправитель уведомлений

    # Сколько мест занято на рейсе (не считая возвращённые билеты)
    def _occupied(self, flight_number):
        count = 0
        for t in self.ticket_repo.all():
            if t.flight_number == flight_number and t.status != TicketStatus.REFUNDED:
                count = count + 1
        return count

    # Бронирование билета
    def book(self, flight_number, passenger):
        flight = self.flight_repo.get(flight_number)
        if flight is None:
            raise ValueError("Рейс не найден")
        if self._occupied(flight_number) >= flight.seats:
            raise ValueError("Нет свободных мест")
        ticket = Ticket(self.ticket_repo.next_id(), flight_number, passenger, TicketStatus.BOOKED)
        self.ticket_repo.add(ticket)
        self.notifier.notify(f"Билет {ticket.id} забронирован для {passenger}")
        return ticket

    # Покупка (оплата) билета
    def purchase(self, ticket_id):
        ticket = self.ticket_repo.get(ticket_id)
        if ticket is None:
            raise ValueError("Билет не найден")
        if ticket.status != TicketStatus.BOOKED:
            raise ValueError("Оплатить можно только забронированный билет")
        flight = self.flight_repo.get(ticket.flight_number)
        self.payment.pay(flight.price)          # используем абстракцию оплаты
        ticket.status = TicketStatus.PAID
        self.notifier.notify(f"Билет {ticket.id} оплачен")
        return ticket

    # Возврат билета
    def refund(self, ticket_id):
        ticket = self.ticket_repo.get(ticket_id)
        if ticket is None:
            raise ValueError("Билет не найден")
        if ticket.status != TicketStatus.PAID:
            raise ValueError("Вернуть можно только оплаченный билет")
        flight = self.flight_repo.get(ticket.flight_number)
        self.payment.refund(flight.price)
        ticket.status = TicketStatus.REFUNDED
        self.notifier.notify(f"Билет {ticket.id} возвращён")
        return ticket

    # Регистрация пассажира по билету
    def register(self, ticket_id):
        ticket = self.ticket_repo.get(ticket_id)
        if ticket is None:
            raise ValueError("Билет не найден")
        if ticket.status != TicketStatus.PAID:
            raise ValueError("Зарегистрировать можно только оплаченный билет")
        ticket.status = TicketStatus.REGISTERED
        self.notifier.notify(f"Пассажир по билету {ticket.id} зарегистрирован")
        return ticket
