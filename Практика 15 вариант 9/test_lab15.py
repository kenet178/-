import pytest
pytest.importorskip('flask')
from datetime import datetime
from sqlalchemy import select
from app import create_app
from app.models import Station
@pytest.fixture
def c(tmp_path):
    app=create_app('sqlite:///'+str(tmp_path/'test.db'))
    with app.extensions['session_factory'].begin() as s:
        s.add_all([Station(name='Москва'),Station(name='Сочи')])
    app.config['TESTING']=True
    with app.test_client() as client:yield client
payload={'number':'РЖД-001','origin_id':1,'destination_id':2,'departure':'2026-12-01T12:00',
         'fare':2000,'seats':50,'status':'scheduled'}
def created(c):return c.post('/api/trains',json=payload)
def test_home(c):assert c.get('/').status_code==200
def test_list(c):assert c.get('/trains').status_code==200
def test_404(c):assert c.get('/unknown').status_code==404
def test_form(c):assert c.get('/trains/create').status_code==200
def test_api_list(c):assert c.get('/api/trains').json==[]
def test_api_create(c):assert created(c).status_code==201
def test_api_detail(c):created(c);assert c.get('/api/trains/1').json['number']=='РЖД-001'
def test_api_absent(c):assert c.get('/api/trains/999').status_code==404
def test_api_duplicate(c):created(c);assert created(c).status_code==409
def test_api_invalid(c):assert c.post('/api/trains',json={'number':'bad'}).status_code==400
def test_api_patch(c):created(c);assert c.patch('/api/trains/1',json={'fare':3000}).json['fare']==3000
def test_api_put(c):created(c);assert c.put('/api/trains/1',json={**payload,'number':'РЖД-002'}).json['number']=='РЖД-002'
def test_api_search(c):created(c);assert len(c.get('/api/trains?q=РЖД-00').json)==1
def test_api_filter(c):created(c);assert c.get('/api/trains?origin_id=2').json==[]
def test_api_sort(c):created(c);assert c.get('/api/trains?sort=fare').status_code==200
def test_web_detail(c):created(c);assert c.get('/trains/1').status_code==200
def test_api_delete(c):created(c);assert c.delete('/api/trains/1').status_code==204
def test_purchase(c):created(c);assert c.post('/api/tickets',json={'train_id':1,'buyer':'Иван','seat':2}).status_code==201
def test_duplicate_seat(c):
    created(c);c.post('/api/tickets',json={'train_id':1,'buyer':'Иван','seat':2})
    assert c.post('/api/tickets',json={'train_id':1,'buyer':'Анна','seat':2}).status_code==409
def test_delete_with_ticket(c):
    created(c);c.post('/api/tickets',json={'train_id':1,'buyer':'Иван','seat':2})
    assert c.delete('/api/trains/1').status_code==409
