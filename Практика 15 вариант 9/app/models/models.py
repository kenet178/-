from datetime import datetime
from sqlalchemy import String,Integer,Float,DateTime,ForeignKey,UniqueConstraint,CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.database import Base
class Station(Base):
    __tablename__='stations'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100),unique=True)
class Train(Base):
    __tablename__='trains'
    id:Mapped[int]=mapped_column(primary_key=True)
    number:Mapped[str]=mapped_column(String(20),unique=True,index=True)
    origin_id:Mapped[int]=mapped_column(ForeignKey('stations.id'))
    destination_id:Mapped[int]=mapped_column(ForeignKey('stations.id'))
    departure:Mapped[datetime]=mapped_column(DateTime)
    fare:Mapped[float]=mapped_column(Float)
    seats:Mapped[int]=mapped_column(Integer)
    status:Mapped[str]=mapped_column(String(20),default='scheduled')
    origin:Mapped[Station]=relationship(foreign_keys=[origin_id])
    destination:Mapped[Station]=relationship(foreign_keys=[destination_id])
    tickets:Mapped[list['Ticket']]=relationship(back_populates='train')
    __table_args__=(CheckConstraint('fare>0'),CheckConstraint('seats>=0'),CheckConstraint('origin_id<>destination_id'))
class Ticket(Base):
    __tablename__='tickets'
    id:Mapped[int]=mapped_column(primary_key=True)
    train_id:Mapped[int]=mapped_column(ForeignKey('trains.id'))
    buyer:Mapped[str]=mapped_column(String(120))
    seat:Mapped[int]=mapped_column(Integer)
    train:Mapped[Train]=relationship(back_populates='tickets')
    __table_args__=(UniqueConstraint('train_id','seat'),CheckConstraint('seat>0'))
