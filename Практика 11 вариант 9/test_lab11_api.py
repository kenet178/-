import pytest
from fastapi.testclient import TestClient
import app as api_module
from database import connect, initialize


@pytest.fixture
def client(tmp_path, monkeypatch):
    path = str(tmp_path / 'api.db')
    with connect(path) as conn: initialize(conn)
    monkeypatch.setattr(api_module, 'DB_PATH', path)
    return TestClient(api_module.app)


def test_get_list(client):
    result = client.get('/flights')
    assert result.status_code == 200 and len(result.json()) == 12


def test_get_search(client):
    result = client.get('/flights', params={'destination':'Казань'})
    assert result.status_code == 200
    assert result.json() and all('Казань' in f['destination'] for f in result.json())


def test_get_missing(client):
    assert client.get('/flights/9999').status_code == 404


def test_stats(client):
    assert client.get('/flights/stats').status_code == 200


def test_create_and_update(client):
    payload={'number':'SU999','origin_id':1,'destination_id':2,'aircraft_id':1,
             'departure':'2026-12-30T09:00','price':4100,'free_seats':3}
    result = client.post('/flights', json=payload)
    assert result.status_code == 201
    fid = result.json()['id']
    update = client.patch(f'/flights/{fid}',json={'price':4500})
    assert update.status_code == 200 and update.json()['price'] == 4500


def test_booking_reduces_seats(client):
    old = client.get('/flights/1').json()['free_seats']
    r=client.post('/tickets',json={'flight_id':1,'passenger_id':1,'seat':'5A'})
    assert r.status_code == 201
    assert client.get('/flights/1').json()['free_seats'] == old - 1


def test_booking_double_seat(client):
    payload={'flight_id':1,'passenger_id':1,'seat':'5A'}
    assert client.post('/tickets',json=payload).status_code == 201
    assert client.post('/tickets',json={**payload,'passenger_id':2}).status_code == 409


def test_delete_created(client):
    payload={'number':'SU998','origin_id':1,'destination_id':2,'aircraft_id':1,
             'departure':'2026-12-31T09:00','price':5100,'free_seats':3}
    fid = client.post('/flights',json=payload).json()['id']
    assert client.delete(f'/flights/{fid}').status_code == 204
    assert client.get(f'/flights/{fid}').status_code == 404


def test_bad_price(client):
    assert client.patch('/flights/1',json={'price':-1}).status_code == 422
