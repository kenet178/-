from datetime import datetime
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base,get_db
from app import app
payload={'number':'SU999','origin':'Москва','destination':'Казань','departure':'2026-12-11T10:00:00',
         'aircraft':'Airbus A320','price':5500,'seats':50,'status':'scheduled'}
@pytest.fixture
def client():
    engine=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    Base.metadata.create_all(engine);maker=sessionmaker(engine)
    def db():
        with maker() as s:yield s
    app.dependency_overrides[get_db]=db
    with TestClient(app) as c:yield c
    app.dependency_overrides.clear();engine.dispose()
def add(c,**kw):return c.post('/flights',json={**payload,**kw})
def test_home(client):assert client.get('/').status_code==200
def test_empty(client):assert client.get('/flights').json()==[]
def test_create(client):assert add(client).status_code==201
def test_create_has_id(client):assert add(client).json()['id']==1
def test_get(client):add(client);assert client.get('/flights/1').json()['number']=='SU999'
def test_get_absent(client):assert client.get('/flights/90').status_code==404
def test_missing_field(client):assert client.post('/flights',json={'number':'bad'}).status_code==422
def test_negative_price(client):assert add(client,price=-1).status_code==422
def test_same_airports(client):assert add(client,destination='Москва').status_code==422
def test_duplicate_number(client):add(client);assert add(client).status_code==409
def test_put(client):add(client);assert client.put('/flights/1',json={**payload,'number':'SU1000'}).json()['number']=='SU1000'
def test_patch(client):add(client);assert client.patch('/flights/1',json={'price':7000}).json()['price']==7000
def test_patch_invalid(client):add(client);assert client.patch('/flights/1',json={'seats':-3}).status_code==422
def test_delete(client):add(client);assert client.delete('/flights/1').status_code==204
def test_delete_repeat(client):add(client);client.delete('/flights/1');assert client.delete('/flights/1').status_code==404
def test_search(client):add(client);assert len(client.get('/flights/search?q=SU999').json())==1
def test_search_empty(client):assert client.get('/flights/search?q=').status_code==422
def test_filter(client):add(client);assert client.get('/flights?status=delayed').json()==[]
def test_sort(client):add(client);add(client,number='SU998',price=4000);assert client.get('/flights?sort=price&direction=desc').json()[0]['number']=='SU999'
def test_sort_error(client):assert client.get('/flights?sort=hack').status_code==400
def test_pagination(client):add(client);add(client,number='SU998');assert len(client.get('/flights?skip=1&limit=1').json())==1
def test_stats(client):add(client);assert client.get('/flights/statistics').json()['total_flights']==1
def test_validation_limit(client):assert client.get('/flights?limit=-1').status_code==422
def test_openapi(client):assert '/flights' in client.get('/openapi.json').json()['paths']
