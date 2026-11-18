from sqlalchemy import select,func,or_
from sqlalchemy.orm import Session,joinedload
from models import Passenger,Train,Ticket,Station
class RailwayRepository:
    def __init__(self,session:Session):self.s=session
    def passenger(self,id:int):return self.s.get(Passenger,id)
    def train(self,id:int):return self.s.get(Train,id)
    def add_passenger(self,name:str,email:str):
        p=Passenger(full_name=name,email=email);self.s.add(p);self.s.flush();return p
    def search_trains(self,q:str='',min_free:int=0,sort:str='departure',desc:bool=False):
        order={'departure':Train.departure,'number':Train.number,'free_seats':Train.free_seats}.get(sort,Train.departure)
        stmt=(select(Train).join(Train.from_station).where(Train.free_seats>=min_free)
              .where(or_(Train.number.ilike(f'%{q}%'),Station.name.ilike(f'%{q}%')))
              .order_by(order.desc() if desc else order.asc()))
        return self.s.scalars(stmt).all()
    def tickets_for(self,passenger_id:int):
        return self.s.scalars(select(Ticket).options(joinedload(Ticket.train)).where(Ticket.passenger_id==passenger_id)).all()
    def counts(self):
        return {'trains':self.s.scalar(select(func.count(Train.id))),
                'tickets':self.s.scalar(select(func.count(Ticket.id))),
                'passengers':self.s.scalar(select(func.count(Passenger.id)))}
    def delete_passenger(self,id:int):
        p=self.passenger(id)
        if p is not None:self.s.delete(p)
        return p is not None
