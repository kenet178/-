# Слой хранения билетов (в памяти)

from models import Ticket


class TicketRepository:
    def __init__(self):
        self._tickets = []
        self._next_id = 1

    def add(self, event, seat, price):
        ticket = Ticket(self._next_id, event, seat, price)
        self._next_id = self._next_id + 1
        self._tickets.append(ticket)
        return ticket

    def all(self):
        return self._tickets

    def get(self, ticket_id):
        for t in self._tickets:
            if t.id == ticket_id:
                return t
        return None

    def remove(self, ticket_id):
        t = self.get(ticket_id)
        if t is None:
            return False
        self._tickets.remove(t)
        return True
