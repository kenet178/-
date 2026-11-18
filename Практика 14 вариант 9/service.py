from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Flight
from repository import FlightRepository
class FlightService:
    def __init__(self,db):self.db=db;self.repo=FlightRepository(db)
    def create(self,data):
        obj=Flight(**data.model_dump());self.db.add(obj)
        self._commit();self.db.refresh(obj);return obj
    def update(self,id:int,data,partial:bool=False):
        obj=self.repo.get(id)
        if obj is None:raise HTTPException(404,'Рейс не найден')
        fields=data.model_dump(exclude_unset=True) if partial else data.model_dump()
        if fields.get('origin',obj.origin)==fields.get('destination',obj.destination):
            raise HTTPException(422,'Аэропорты должны отличаться')
        for key,val in fields.items():
            if val is not None:setattr(obj,key,val)
        self._commit();self.db.refresh(obj);return obj
    def delete(self,id:int):
        obj=self.repo.get(id)
        if obj is None:raise HTTPException(404,'Рейс не найден')
        self.db.delete(obj);self._commit()
    def _commit(self):
        try:self.db.commit()
        except IntegrityError as e:
            self.db.rollback();raise HTTPException(409,'Номер рейса занят или нарушено ограничение') from e
