from sqlalchemy import update,delete,select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from models import Train,Passenger,Ticket
class RailwayError(ValueError):pass
class RailwayService:
    def __init__(self,session:Session):self.s=session
    def purchase(self,train_id:int,passenger_id:int,seat:int,price:int=2500) -> Ticket:
        if seat<=0 or price<=0:raise RailwayError('Место и цена должны быть положительными')
        try:
            with self.s.begin():
                if self.s.get(Passenger,passenger_id) is None:raise RailwayError('Пассажир не найден')
                train=self.s.get(Train,train_id)
                if train is None:raise RailwayError('Поезд не найден')
                if seat>train.capacity:raise RailwayError('Место выходит за вместимость поезда')
                changed=self.s.execute(update(Train).where(Train.id==train_id,Train.free_seats>0).values(free_seats=Train.free_seats-1))
                if changed.rowcount!=1:raise RailwayError('Нет свободных мест')
                ticket=Ticket(train_id=train_id,passenger_id=passenger_id,seat=seat,price=price)
                self.s.add(ticket);self.s.flush()
            return ticket
        except IntegrityError as e:
            self.s.rollback();raise RailwayError('Место занято или нарушена целостность') from e
    def cancel(self,ticket_id:int)->bool:
        with self.s.begin():
            statement = delete(Ticket).where(Ticket.id == ticket_id).returning(Ticket.train_id)
            train_id = self.s.scalar(statement)
            if train_id is None:
                return False
            self.s.execute(update(Train).where(Train.id == train_id).values(free_seats=Train.free_seats + 1))
        return True
    def rename_passenger(self,id:int,name:str):
        if not name.strip():raise RailwayError('Имя обязательно')
        with self.s.begin():
            p=self.s.get(Passenger,id)
            if p is None:raise RailwayError('Пассажир не найден')
            p.full_name=name
        return p
