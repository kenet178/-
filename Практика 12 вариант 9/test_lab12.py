import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine,func,select
from database import Base
from models import Station,Train,Passenger,Ticket
from repository import RailwayRepository
from service import RailwayService,RailwayError
@pytest.fixture
def maker():
    e=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    Base.metadata.create_all(e)
    sf=sessionmaker(e,expire_on_commit=False)
    with sf.begin() as s:
        s.add_all([Station(name='Москва'),Station(name='Казань'),Passenger(full_name='Иван',email='i@test.org')])
        s.flush();s.add(Train(number='001',from_station_id=1,to_station_id=2,departure=__import__('datetime').datetime(2026,12,1),capacity=10,free_seats=10))
    yield sf;e.dispose()
def test_list(maker):
    with maker() as s:assert len(RailwayRepository(s).search_trains())==1
def test_filter(maker):
    with maker() as s:assert len(RailwayRepository(s).search_trains(min_free=11))==0
def test_search_station(maker):
    with maker() as s:assert len(RailwayRepository(s).search_trains('Моск'))==1
def test_get(maker):
    with maker() as s:assert RailwayRepository(s).train(1).number=='001'
def test_passenger(maker):
    with maker() as s:assert RailwayRepository(s).passenger(1).email=='i@test.org'
def test_purchase(maker):
    with maker() as s:
        t=RailwayService(s).purchase(1,1,2);assert t.id
    with maker() as s:assert RailwayRepository(s).train(1).free_seats==9
def test_unique_seat_rollback(maker):
    with maker() as s:RailwayService(s).purchase(1,1,2)
    with maker() as s:
        with pytest.raises(RailwayError):RailwayService(s).purchase(1,1,2)
    with maker() as s:assert RailwayRepository(s).train(1).free_seats==9
def test_invalid_seat(maker):
    with maker() as s:
        with pytest.raises(RailwayError):RailwayService(s).purchase(1,1,100)
def test_invalid_passenger(maker):
    with maker() as s:
        with pytest.raises(RailwayError):RailwayService(s).purchase(1,999,1)
def test_cancel(maker):
    with maker() as s:t=RailwayService(s).purchase(1,1,2);id=t.id
    with maker() as s:assert RailwayService(s).cancel(id)
    with maker() as s:assert RailwayRepository(s).train(1).free_seats==10
def test_cancel_missing(maker):
    with maker() as s:assert RailwayService(s).cancel(999) is False
def test_related(maker):
    with maker() as s:t=RailwayService(s).purchase(1,1,3)
    with maker() as s:assert RailwayRepository(s).tickets_for(1)[0].train.number=='001'
def test_rename(maker):
    with maker() as s:RailwayService(s).rename_passenger(1,'Новый')
    with maker() as s:assert RailwayRepository(s).passenger(1).full_name=='Новый'
def test_stats(maker):
    with maker() as s:assert RailwayRepository(s).counts()['trains']==1
