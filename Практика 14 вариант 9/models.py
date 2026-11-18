from datetime import datetime
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Float,Integer,DateTime,CheckConstraint
from database import Base
class Flight(Base):
    __tablename__='flights'
    id:Mapped[int]=mapped_column(primary_key=True)
    number:Mapped[str]=mapped_column(String(16),unique=True,index=True)
    origin:Mapped[str]=mapped_column(String(80),index=True)
    destination:Mapped[str]=mapped_column(String(80),index=True)
    departure:Mapped[datetime]=mapped_column(DateTime,index=True)
    aircraft:Mapped[str]=mapped_column(String(80))
    price:Mapped[float]=mapped_column(Float)
    seats:Mapped[int]=mapped_column(Integer)
    status:Mapped[str]=mapped_column(String(24),default='scheduled')
    __table_args__=(CheckConstraint('price>0'),CheckConstraint('seats>=0'),CheckConstraint('origin<>destination'))
