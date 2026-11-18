from service import FlightService
class Repo:
    def __init__(self):self.data={'SU101':{'number':'SU101','origin':'Москва','destination':'Казань','aircraft':{'model':'Airbus A320'},'status':'scheduled'}}
    def one(self,k):return self.data.get(k)
    def create(self,d):self.data[d['number']]=d;return 'id'
    def update(self,n,d):self.data[n].update(d);return 1
    def delete(self,n):return self.data.pop(n,None) is not None
    def all(self):return list(self.data.values())
class Cache:
    def __init__(self):self.data={};self.searches=[]
    def get_flight(self,n):return self.data.get(n)
    def cache_flight(self,n,d,ttl=60):self.data[n]=d.copy()
    def invalidate(self,n):self.data.pop(n,None)
    def record_search(self,q):self.searches.append(q)

def test_cache_miss_hit():
    s=FlightService(Repo(),Cache());assert s.get('SU101')[1]=='miss';assert s.get('SU101')[1]=='hit'
def test_unknown():assert FlightService(Repo(),Cache()).get('none')==(None,'miss')
def test_invalidate_update():
    s=FlightService(Repo(),Cache());s.get('SU101');s.change('SU101',{'status':'delayed'})
    assert s.get('SU101')[1]=='miss' and s.get('SU101')[0]['status']=='delayed'
def test_invalidate_delete():
    s=FlightService(Repo(),Cache());s.get('SU101');s.delete('SU101');assert s.get('SU101')[0] is None
def test_create():
    s=FlightService(Repo(),Cache());s.add({'number':'SU202','origin':'Сочи','destination':'Москва','aircraft':{'model':'Boeing 737'}});assert s.get('SU202')[0]['origin']=='Сочи'
def test_search():
    s=FlightService(Repo(),Cache());assert len(s.search('Моск'))==1
