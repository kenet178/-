import sqlite3
from repository import FlightRepository
from exceptions import BookingError, ValidationError, FlightNotFoundError
class AirlineService:
    def __init__(self,conn: sqlite3.Connection):
        self.conn=conn;self.flights=FlightRepository(conn)
    def book(self,flight_id: int,passenger_id: int,seat: str) -> dict:

        if not seat or len(seat)>5: raise BookingError('Некорректное место')
        try:
            self.conn.execute('BEGIN IMMEDIATE')
            changed=self.conn.execute('UPDATE flights SET free_seats=free_seats-1 WHERE id=? AND free_seats>0',(flight_id,)).rowcount
            if not changed: raise BookingError('Рейс не найден или нет мест')
            cur=self.conn.execute('INSERT INTO tickets(flight_id,passenger_id,seat) VALUES(?,?,?)',(flight_id,passenger_id,seat))
            self.conn.execute('COMMIT')
            return {'ticket_id':cur.lastrowid,'flight_id':flight_id,'passenger_id':passenger_id,'seat':seat}
        except (BookingError,sqlite3.Error) as e:
            if self.conn.in_transaction:
                self.conn.rollback()
            raise BookingError(str(e)) from e

class FlightService:

    def __init__(self, repository: FlightRepository):
        self.repository = repository

    def list_flights(self, destination: str | None = None):
        return self.repository.all(destination)

    def get_flight(self, flight_id: int):
        flight = self.repository.get(flight_id)
        if flight is None:
            raise FlightNotFoundError('Рейс не найден')
        return flight

    def create_flight(self, data: dict):
        if not str(data.get('number','')).strip() or float(data.get('price',0)) <= 0:
            raise ValidationError('Укажите номер рейса и положительную цену')
        if data.get('origin_id') == data.get('destination_id'):
            raise ValidationError('Аэропорты должны отличаться')
        return self.repository.create(**data)

    def change_price(self, flight_id: int, price: float):
        if price <= 0: raise ValidationError('Цена должна быть положительной')
        if not self.repository.update_price(flight_id, price):
            raise FlightNotFoundError('Рейс не найден')
        return self.get_flight(flight_id)

    def delete_flight(self, flight_id: int):
        if not self.repository.delete(flight_id):
            raise FlightNotFoundError('Рейс не найден')
