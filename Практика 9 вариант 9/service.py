# Слой бизнес-логики: операции над билетами

from repository import TicketRepository


class TicketService:
    def __init__(self):
        self.repo = TicketRepository()
        # начальные данные
        self.repo.add("Концерт", "A1", 2000)
        self.repo.add("Концерт", "A2", 2000)
        self.repo.add("Театр", "B1", 1500)

    def list_all(self):
        return [t.to_dict() for t in self.repo.all()]

    def get(self, ticket_id):
        t = self.repo.get(ticket_id)
        return t.to_dict() if t is not None else None

    def create(self, event, seat, price):
        t = self.repo.add(event, seat, int(price))
        return t.to_dict()

    # продажа билета
    def buy(self, ticket_id):
        t = self.repo.get(ticket_id)
        if t is None:
            return None
        if t.status == "продан":
            return "sold"
        t.status = "продан"
        return t.to_dict()

    # СПЕЦИАЛИЗИРОВАННАЯ КОМАНДА: проверка доступных (свободных) мест
    def available(self, event=None):
        result = []
        for t in self.repo.all():
            if t.status == "свободен" and (event is None or t.event == event):
                result.append(t.to_dict())
        return result

    def delete(self, ticket_id):
        return self.repo.remove(ticket_id)
