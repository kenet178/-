from datetime import datetime
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from app.models import Train,Ticket,Station
from app.repositories import TrainRepository
class DomainError(ValueError):pass
class TrainService:
    def __init__(self,db):self.db=db;self.repo=TrainRepository(db)
    def validate(self,data):
        try:
            record={
                'number':str(data['number']).strip(),
                'origin_id':int(data['origin_id']),'destination_id':int(data['destination_id']),
                'departure':datetime.fromisoformat(str(data['departure'])),
                'fare':float(data['fare']),'seats':int(data['seats']),
                'status':str(data.get('status','scheduled'))
            }
        except (KeyError,ValueError,TypeError) as e:raise DomainError('Неверные данные поезда') from e
        if len(record['number'])<2 or record['fare']<=0 or record['seats']<0 or record['origin_id']==record['destination_id']:
            raise DomainError('Проверьте номер, цену, места и маршрут')
        if self.db.get(Station,record['origin_id']) is None or self.db.get(Station,record['destination_id']) is None:
            raise DomainError('Станция не существует')
        return record
    def save(self,data,id=None):
        validated=self.validate(data)
        if id is None:obj=Train(**validated);self.db.add(obj)
        else:
            obj=self.repo.get(id)
            if obj is None:raise DomainError('Поезд не найден')
            for k,v in validated.items():setattr(obj,k,v)
        try:self.db.commit();self.db.refresh(obj);return obj
        except IntegrityError as e:
            self.db.rollback();raise DomainError('Номер поезда уже занят или данные некорректны') from e
    def remove(self,id):
        obj=self.repo.get(id)
        if not obj:raise DomainError('Поезд не найден')
        if self.repo.tickets(id):raise DomainError('Нельзя удалить поезд с проданными билетами')
        self.db.delete(obj);self.db.commit()
    def purchase(self,train_id,buyer,seat):
        if not buyer or not buyer.strip():raise DomainError('Введите имя покупателя')
        try:seat=int(seat)
        except (ValueError,TypeError) as e:raise DomainError('Неверное место') from e
        try:
            train=self.repo.get(train_id)
            if train is None:raise DomainError('Поезд не найден')
            if seat<1 or seat>50:raise DomainError('Место должно быть от 1 до 50')
            if self.db.execute(update(Train).where(Train.id==train_id,Train.seats>0).values(seats=Train.seats-1)).rowcount!=1:
                raise DomainError('Места закончились')
            ticket=Ticket(train_id=train_id,buyer=buyer.strip(),seat=seat)
            self.db.add(ticket);self.db.commit();self.db.refresh(ticket);return ticket
        except (IntegrityError,DomainError) as e:
            self.db.rollback()
            if isinstance(e,IntegrityError):raise DomainError('Это место уже занято') from e
            raise
