from pymongo import MongoClient,ASCENDING,DESCENDING
from config import MONGO_URL,MONGO_DB
class MongoRepository:
    def __init__(self,client=None):
        self.client=client or MongoClient(MONGO_URL,serverSelectionTimeoutMS=3000)
        self.collection=self.client[MONGO_DB]['flights']
    def indexes(self):
        self.collection.create_index('number',unique=True,name='unique_number')
        self.collection.create_index([('departure',ASCENDING),('status',ASCENDING)],name='schedule_status')
        self.collection.create_index('origin',name='origin_search')
    def create(self,data:dict):return str(self.collection.insert_one(data.copy()).inserted_id)
    def one(self,number:str):return self.collection.find_one({'number':number},{'_id':0})
    def all(self,limit:int=100):return list(self.collection.find({},{'_id':0}).limit(limit))
    def update(self,number:str,changes:dict):
        changes={k:v for k,v in changes.items() if k not in ('_id','number')}
        return self.collection.update_one({'number':number},{'$set':changes}).modified_count
    def delete(self,number:str):return self.collection.delete_one({'number':number}).deleted_count
    def upcoming(self, from_date):
        query = {'departure': {'$gte': from_date}, 'status': {'$in': ['scheduled', 'delayed', 'boarding']}}
        cursor = self.collection.find(query, {'_id': 0}).sort('departure', ASCENDING).limit(10)
        return list(cursor)

    def queries(self):
        c=self.collection
        return {
            'status_scheduled':list(c.find({'status':'scheduled'},{'_id':0})),
            'origin_moscow':list(c.find({'origin':'Москва'},{'_id':0})),
            'seats_gt_50':list(c.find({'seats':{'$gt':50}},{'_id':0})),
            'by_departure_asc':list(c.find({},{'_id':0}).sort('departure',ASCENDING)),
            'by_seats_desc':list(c.find({},{'_id':0}).sort('seats',DESCENDING)),
            'first_five':list(c.find({},{'_id':0}).limit(5)),
            'aircraft_model':list(c.find({'aircraft.model':'Airbus A320'},{'_id':0})),
            'passenger_in_array':list(c.find({'passengers.name':'Иван Петров'},{'_id':0})),
            'count_by_status':list(c.aggregate([{'$group':{'_id':'$status','count':{'$sum':1}}}])),
            'avg_seats_by_origin':list(c.aggregate([{'$group':{'_id':'$origin','avg_seats':{'$avg':'$seats'}}}])),
            'combined':list(c.find({'status':'scheduled','seats':{'$gt':20}},{'_id':0}))
        }
