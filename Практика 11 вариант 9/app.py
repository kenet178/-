from contextlib import closing
import os,sqlite3
from pathlib import Path
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from database import connect, initialize
from repository import FlightRepository
from service import AirlineService,BookingError
from redis_cache import RedisFlightSearchCache

app=FastAPI(title='ЛР11 / Авиакомпания / SQL без ORM',version='1.0')
DB_PATH=os.getenv('DATABASE_PATH',str(Path(__file__).resolve().parent / 'airline.db'))
with closing(connect(DB_PATH)) as c: initialize(c)
class FlightIn(BaseModel):
    number:str=Field(min_length=3);origin_id:int;destination_id:int;aircraft_id:int
    departure:str;price:float=Field(gt=0);free_seats:int=Field(ge=0)
class BookingIn(BaseModel):
    flight_id:int;passenger_id:int;seat:str=Field(min_length=1,max_length=5)
class PriceIn(BaseModel): price:float=Field(gt=0)
@app.get('/flights')
def list_flights(destination: str|None=None):
    cache = RedisFlightSearchCache()
    result = cache.get(destination)
    if result is not None: return result
    with closing(connect(DB_PATH)) as c: result = FlightRepository(c).all(destination)
    cache.set(destination, result)
    return result
@app.get('/flights/stats')
def stats():
    with closing(connect(DB_PATH)) as c:return FlightRepository(c).stats()
@app.get('/flights/{flight_id}')
def get_flight(flight_id:int):
    with closing(connect(DB_PATH)) as c: result=FlightRepository(c).get(flight_id)
    if result is None:raise HTTPException(404,'Рейс не найден')
    return result
@app.post('/flights',status_code=201)
def create_flight(data:FlightIn):
    try:
        with closing(connect(DB_PATH)) as c: result = FlightRepository(c).create(**data.model_dump())
        RedisFlightSearchCache().invalidate_all()
        return result
    except sqlite3.IntegrityError as e:raise HTTPException(409,str(e)) from e
@app.patch('/flights/{flight_id}')
def patch_flight(flight_id:int,data:PriceIn):
    with closing(connect(DB_PATH)) as c:
        repo=FlightRepository(c)
        if not repo.update_price(flight_id,data.price):raise HTTPException(404,'Рейс не найден')
        result = repo.get(flight_id)
        RedisFlightSearchCache().invalidate_all()
        return result
@app.delete('/flights/{flight_id}',status_code=204)
def remove_flight(flight_id:int):
    try:
        with closing(connect(DB_PATH)) as c:
            if not FlightRepository(c).delete(flight_id):raise HTTPException(404,'Рейс не найден')
        RedisFlightSearchCache().invalidate_all()
    except sqlite3.IntegrityError as e:raise HTTPException(409,'Есть связанные билеты') from e
@app.post('/tickets',status_code=201)
def book_ticket(data:BookingIn):
    try:
        with closing(connect(DB_PATH)) as c:
            result = AirlineService(c).book(**data.model_dump())
        RedisFlightSearchCache().invalidate_all()
        return result
    except BookingError as e:raise HTTPException(409,str(e)) from e
