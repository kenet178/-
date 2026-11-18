import pytest
from database import connect, initialize
from repository import FlightRepository
from service import AirlineService,BookingError
@pytest.fixture
def db(tmp_path):
    c=connect(str(tmp_path/'test.db'));initialize(c);yield c;c.close()
def test_seed_12(db):assert len(FlightRepository(db).all())==12
def test_related_rows(db):assert db.execute('SELECT COUNT(*) FROM airports').fetchone()[0]>=5
def test_aircraft(db):assert db.execute('SELECT COUNT(*) FROM aircraft').fetchone()[0]>=3
def test_filter(db):assert len(FlightRepository(db).all('Санкт'))>=1
def test_get(db):assert FlightRepository(db).get(1)['number']=='SU101'
def test_get_missing(db):assert FlightRepository(db).get(999) is None
def test_create(db):assert FlightRepository(db).create('SU999',1,2,1,'2026-12-20T08:00',6000,5)['number']=='SU999'
def test_update(db):assert FlightRepository(db).update_price(1,9000) and FlightRepository(db).get(1)['price']==9000
def test_delete(db):assert FlightRepository(db).delete(1) and FlightRepository(db).get(1) is None
def test_stats(db):assert sum(x['flights'] for x in FlightRepository(db).stats())==12
def test_booking(db):
    before=FlightRepository(db).get(1)['free_seats'];t=AirlineService(db).book(1,1,'1A')
    assert t['ticket_id']>0 and FlightRepository(db).get(1)['free_seats']==before-1
def test_booking_rollback(db):
    AirlineService(db).book(1,1,'1A');before=FlightRepository(db).get(1)['free_seats']
    with pytest.raises(BookingError):AirlineService(db).book(1,1,'1B')
    assert FlightRepository(db).get(1)['free_seats']==before
def test_wrong_flight(db):
    with pytest.raises(BookingError):AirlineService(db).book(999,1,'1A')
def test_foreign_keys(db):
    with pytest.raises(BookingError):AirlineService(db).book(1,999,'1A')
def test_sql_injection_safe(db):assert FlightRepository(db).all("' OR 1=1 --")==[]
