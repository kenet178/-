from sqlalchemy import Integer,String,ForeignKey,CheckConstraint,UniqueConstraint,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from database import Base
from datetime import datetime
class Station(Base):
    __tablename__='stations'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
class Passenger(Base):
    __tablename__='passengers'
    id:Mapped[int]=mapped_column(primary_key=True)
    full_name:Mapped[str]=mapped_column(String(120),nullable=False)
    email:Mapped[str]=mapped_column(String(160),unique=True,nullable=False)
    tickets:Mapped[list['Ticket']]=relationship(back_populates='passenger')
class Train(Base):
    __tablename__='trains'
    id:Mapped[int]=mapped_column(primary_key=True)
    number:Mapped[str]=mapped_column(String(20),unique=True,nullable=False)
    from_station_id:Mapped[int]=mapped_column(ForeignKey('stations.id'),nullable=False)
    to_station_id:Mapped[int]=mapped_column(ForeignKey('stations.id'),nullable=False)
    departure:Mapped[datetime]=mapped_column(DateTime,nullable=False)
    capacity:Mapped[int]=mapped_column(Integer,nullable=False)
    free_seats:Mapped[int]=mapped_column(Integer,nullable=False)
    from_station:Mapped[Station]=relationship(foreign_keys=[from_station_id])
    to_station:Mapped[Station]=relationship(foreign_keys=[to_station_id])
    tickets:Mapped[list['Ticket']]=relationship(back_populates='train')
    __table_args__=(CheckConstraint('capacity>0'),CheckConstraint('free_seats>=0'),CheckConstraint('from_station_id<>to_station_id'))
class Ticket(Base):
    __tablename__='tickets'
    id:Mapped[int]=mapped_column(primary_key=True)
    passenger_id:Mapped[int]=mapped_column(ForeignKey('passengers.id'),nullable=False)
    train_id:Mapped[int]=mapped_column(ForeignKey('trains.id'),nullable=False)
    seat:Mapped[int]=mapped_column(Integer,nullable=False)
    price:Mapped[int]=mapped_column(Integer,nullable=False)
    passenger:Mapped[Passenger]=relationship(back_populates='tickets')
    train:Mapped[Train]=relationship(back_populates='tickets')
    __table_args__=(UniqueConstraint('train_id','seat'),CheckConstraint('seat>0'),CheckConstraint('price>0'))
