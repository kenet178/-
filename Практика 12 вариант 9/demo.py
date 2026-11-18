import tempfile
from pathlib import Path
import os
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from database import Base, make_engine
from models import Station, Passenger, Train, Ticket
from service import RailwayService, RailwayError
from repository import RailwayRepository
from datetime import datetime, timedelta


def main():
    print('=== ПРАКТИКА 12. ВАРИАНТ 9: Ж/Д БИЛЕТЫ ===')
    with tempfile.TemporaryDirectory() as folder:
        engine = make_engine(os.getenv('DATABASE_URL') or f'sqlite:///{Path(folder) / "railway.db"}')
        try:
            run(engine)
        finally:
            engine.dispose()
    print('Демонстрация завершена успешно.')


def run(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    suffix = uuid4().hex[:10]
    with Session.begin() as s:
        stations = []
        for name in ('Москва', 'Казань'):
            station = s.scalar(select(Station).where(Station.name == name))
            if station is None:
                station = Station(name=name)
                s.add(station)
            stations.append(station)
        a, b = stations
        s.flush()
        passenger = Passenger(full_name='Александр Петров', email=f'alex.demo.{suffix}@example.org')
        train = Train(number=f'РЖД-{suffix}', from_station_id=a.id, to_station_id=b.id,
                      departure=datetime.now() + timedelta(days=7), capacity=30, free_seats=30)
        s.add_all([passenger, train])
        s.flush()
        passenger_id, train_id = passenger.id, train.id
    with Session() as s:
        print('SEARCH:', [(t.number, t.free_seats) for t in RailwayRepository(s).search_trains('РЖД')])
    with Session() as s:
        ticket = RailwayService(s).purchase(train_id, passenger_id, 7)
        ticket_id = ticket.id
        print('PURCHASE:', ticket.id, ticket.seat, ticket.price)
    with Session() as s:
        try:
            RailwayService(s).purchase(train_id, passenger_id, 7)
        except RailwayError as err: print('DUPLICATE:', err)
    with Session() as s:
        print('TICKETS:', [(t.id,t.seat) for t in RailwayRepository(s).tickets_for(passenger_id)])
    with Session() as s:
        print('CANCEL:', RailwayService(s).cancel(ticket_id))
    with Session() as s:
        print('FREE:', RailwayRepository(s).train(train_id).free_seats)

if __name__ == '__main__':main()
