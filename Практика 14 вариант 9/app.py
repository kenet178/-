import logging,time
from fastapi import FastAPI,Depends,HTTPException,Query,Response
from sqlalchemy.orm import Session
from database import Base,engine,get_db
from models import Flight
from schemas import FlightCreate,FlightPut,FlightPatch,FlightOut,Status
from service import FlightService
from repository import FlightRepository
Base.metadata.create_all(bind=engine)
app=FastAPI(title='ЛР14 — авиарейсы (вариант 9)',version='1.0.0')
log=logging.getLogger('airline.lab14')
@app.middleware('http')
async def access(request,call_next):
    start=time.perf_counter()
    response=await call_next(request)
    log.info('%s %s -> %s (%.1f ms)',request.method,request.url.path,response.status_code,(time.perf_counter()-start)*1000)
    return response
@app.get('/')
async def home():return {'project':'Авиакомпания','docs':'/docs','resources':'/flights'}
@app.get('/flights',response_model=list[FlightOut])
def list_flights(q:str='',status:Status|None=None,origin:str|None=None,
                 sort:str='departure',direction:str='asc',skip:int=Query(0,ge=0),limit:int=Query(20,ge=1,le=100),db:Session=Depends(get_db)):
    if sort not in ('departure','price','seats','number') or direction not in ('asc','desc'):
        raise HTTPException(400,'Недопустимая сортировка')
    return FlightRepository(db).all(q,status,origin,sort,direction,skip,limit)
@app.get('/flights/search',response_model=list[FlightOut])
async def search(q:str=Query(min_length=1),db:Session=Depends(get_db)):
    return FlightRepository(db).all(q=q)
@app.get('/flights/statistics')
def statistics(db:Session=Depends(get_db)):
    return FlightRepository(db).stats()
@app.get('/flights/{flight_id}',response_model=FlightOut)
def one(flight_id:int,db:Session=Depends(get_db)):
    obj=FlightRepository(db).get(flight_id)
    if obj is None:raise HTTPException(404,'Рейс не найден')
    return obj
@app.post('/flights',response_model=FlightOut,status_code=201)
def add(data:FlightCreate,db:Session=Depends(get_db)):return FlightService(db).create(data)
@app.put('/flights/{flight_id}',response_model=FlightOut)
def replace(flight_id:int,data:FlightPut,db:Session=Depends(get_db)):
    return FlightService(db).update(flight_id,data)
@app.patch('/flights/{flight_id}',response_model=FlightOut)
def patch(flight_id:int,data:FlightPatch,db:Session=Depends(get_db)):
    return FlightService(db).update(flight_id,data,partial=True)
@app.delete('/flights/{flight_id}',status_code=204)
def delete(flight_id:int,db:Session=Depends(get_db)):
    FlightService(db).delete(flight_id);return Response(status_code=204)
