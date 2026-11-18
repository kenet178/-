import os
import tempfile
from pathlib import Path


def main():
    print('=== ПРАКТИКА 14. ВАРИАНТ 9: FASTAPI / FLIGHTS ===')
    with tempfile.TemporaryDirectory() as folder:
        os.environ['DATABASE_URL'] = 'sqlite:///' + str(Path(folder) / 'demo.db')

        from fastapi.testclient import TestClient
        from app import app
        client = TestClient(app)
        data1 = {'number':'SU501','origin':'Москва','destination':'Казань','departure':'2026-12-17T10:00:00',
                 'aircraft':'Airbus A320','price':7900,'seats':100,'status':'scheduled'}
        data2 = {'number':'SU502','origin':'Казань','destination':'Сочи','departure':'2026-12-18T08:00:00',
                 'aircraft':'Boeing 737','price':6900,'seats':80,'status':'delayed'}
        for x in (data1,data2):print('POST:',client.post('/flights',json=x).status_code)
        print('LIST:',client.get('/flights').json())
        print('SEARCH:',client.get('/flights/search',params={'q':'SU501'}).json())
        print('FILTER:',client.get('/flights',params={'status':'scheduled'}).json())
        print('SORT:',client.get('/flights',params={'sort':'price','direction':'desc'}).json())
        print('PAGINATION:',client.get('/flights',params={'skip':0,'limit':1}).json())
        print('STATS:',client.get('/flights/statistics').json())
        print('PATCH:',client.patch('/flights/1',json={'price':8000}).status_code)
        print('404:',client.get('/flights/999').status_code)
        print('DELETE:',client.delete('/flights/2').status_code)
        print('OPENAPI:',client.get('/openapi.json').status_code)
        print('Демонстрация завершена успешно.')

if __name__ == '__main__':main()
