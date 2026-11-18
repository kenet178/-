from mongo_repository import MongoRepository
from datetime import datetime, timedelta
from models import Flight
from pymongo.errors import PyMongoError

def seed():
    repo=MongoRepository();repo.indexes()
    airports=['Москва','Казань','Сочи','Санкт-Петербург','Екатеринбург']
    first_departure = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    for i in range(20):
        f=Flight(number=f'SU{100+i}',origin=airports[i%5],destination=airports[(i+1)%5],
                 aircraft={'model':['Airbus A320','Boeing 737'][i%2],'board':f'RA-{7000+i}'},
                 passengers=[{'name':'Иван Петров','seat':'1A'}] if i%3==0 else [{'name':'Ольга','seat':'2B'}],
                 seats=60+i,status='scheduled' if i%4 else 'delayed',departure=(first_departure + timedelta(days=i)).isoformat())
        repo.collection.update_one({'number':f.number},{'$setOnInsert':f.as_document()},upsert=True)
    print('MongoDB: документов',repo.collection.count_documents({}))
if __name__=='__main__':seed()
