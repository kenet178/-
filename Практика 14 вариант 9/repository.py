from sqlalchemy.orm import Session
from sqlalchemy import select,func
from models import Flight
class FlightRepository:
    def __init__(self,db:Session):self.db=db
    def get(self,id:int):return self.db.get(Flight,id)
    def get_by_number(self,num:str):return self.db.scalar(select(Flight).where(Flight.number==num))
    def all(self,q:str='',status:str|None=None,origin:str|None=None,sort:str='departure',direction:str='asc',skip:int=0,limit:int=20):
        stmt=select(Flight)
        if q:stmt=stmt.where(Flight.number.ilike(f'%{q}%'))
        if status:stmt=stmt.where(Flight.status==status)
        if origin:stmt=stmt.where(Flight.origin.ilike(f'%{origin}%'))
        col={'departure':Flight.departure,'price':Flight.price,'seats':Flight.seats,'number':Flight.number}.get(sort,Flight.departure)
        return list(self.db.scalars(stmt.order_by(col.desc() if direction=='desc' else col.asc()).offset(skip).limit(limit)))
    def stats(self):
        total=self.db.scalar(select(func.count(Flight.id))) or 0
        avg=self.db.scalar(select(func.avg(Flight.price))) or 0
        free=self.db.scalar(select(func.sum(Flight.seats))) or 0
        grouped=self.db.execute(select(Flight.status,func.count(Flight.id)).group_by(Flight.status)).all()
        return {'total_flights':total,'average_price':round(float(avg),2),'free_seats':int(free),
                'by_status':{k:v for k,v in grouped}}
