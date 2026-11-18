from sqlalchemy import select,or_
from sqlalchemy.orm import joinedload
from app.models import Train,Ticket,Station
class TrainRepository:
    def __init__(self,db):self.db=db
    def get(self,id):return self.db.get(Train,id)
    def list(self,q='',origin_id=None,destination_id=None,sort='departure',direction='asc'):
        stmt=select(Train).options(joinedload(Train.origin),joinedload(Train.destination))
        if q:stmt=stmt.where(Train.number.ilike('%'+q+'%'))
        if origin_id:stmt=stmt.where(Train.origin_id==origin_id)
        if destination_id:stmt=stmt.where(Train.destination_id==destination_id)
        col={'departure':Train.departure,'fare':Train.fare,'number':Train.number}.get(sort,Train.departure)
        return list(self.db.scalars(stmt.order_by(col.desc() if direction=='desc' else col.asc())))
    def stations(self):return list(self.db.scalars(select(Station).order_by(Station.name)))
    def tickets(self,train_id):return list(self.db.scalars(select(Ticket).where(Ticket.train_id==train_id)))
