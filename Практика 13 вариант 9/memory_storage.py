from copy import deepcopy


class MemoryMongoRepository:
    def __init__(self): self.docs = {}
    def create(self, data):
        number = data['number']
        if number in self.docs: raise ValueError('Дубликат рейса')
        self.docs[number] = deepcopy(data)
        return number
    def one(self, number): return deepcopy(self.docs.get(number))
    def all(self, limit=100): return [deepcopy(x) for x in self.docs.values()][:limit]
    def upcoming(self, from_date):
        active = {'scheduled', 'delayed', 'boarding'}
        flights = [
            doc for doc in self.docs.values()
            if doc['departure'] >= from_date and doc['status'] in active
        ]
        return deepcopy(sorted(flights, key=lambda doc: doc['departure'])[:10])

    def update(self, number, changes):
        if number not in self.docs: return 0
        self.docs[number].update({k:v for k,v in changes.items() if k != 'number'})
        return 1
    def delete(self, number): return int(self.docs.pop(number, None) is not None)


class MemoryRedisCache:
    def __init__(self): self.items = {}; self.searches = []
    def get_flight(self, number): return deepcopy(self.items.get(number))
    def cache_flight(self, number, doc, ttl=60): self.items[number] = deepcopy(doc)
    def invalidate(self, number): self.items.pop(number, None)
    def record_search(self, query): self.searches.append(query)
    def upcoming(self, repository, from_date):
        return repository.upcoming(from_date)
