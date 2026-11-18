from datetime import datetime
from time import perf_counter

from models import Flight
class FlightService:
    def __init__(self,repository,cache):
        self.repo=repository;self.cache=cache
    def get(self,number):
        cached=self.cache.get_flight(number)
        if cached is not None:return cached,'hit'
        item=self.repo.one(number)
        if item:self.cache.cache_flight(number,item)
        return item,'miss'
    def add(self,data):
        document = Flight(**data).as_document()
        flight_id = self.repo.create(document)
        self.cache.invalidate(document['number'])
        return flight_id
    def change(self,number,changes):
        current = self.repo.one(number)
        if current is None:
            return 0
        changes = {key: value for key, value in changes.items() if key not in ('_id', 'number')}
        if not changes:
            return 0
        document = Flight(**(current | changes)).as_document()
        changes = {key: document[key] for key in changes}
        updated=self.repo.update(number,changes)
        self.cache.invalidate(number)
        return updated
    def delete(self,number):
        result=self.repo.delete(number)
        self.cache.invalidate(number)
        return result
    def search(self,term):
        self.cache.record_search(term)
        term = term.casefold()
        return [
            doc for doc in self.repo.all()
            if any(term in doc[field].casefold() for field in ('number', 'origin', 'destination'))
        ]

    def upcoming(self):
        return self.cache.upcoming(self.repo, datetime.now().isoformat(timespec='seconds'))
    def benchmark(self,number,repeats=20):
        if self.repo.one(number) is None:
            raise ValueError('Рейс не найден')
        start = perf_counter()
        for _ in range(repeats):
            self.repo.one(number)
        mongo_avg = (perf_counter() - start) * 1000 / repeats
        self.cache.invalidate(number)
        a=perf_counter();self.get(number);cold=(perf_counter()-a)*1000
        a=perf_counter()
        for _ in range(repeats):self.get(number)
        warm=(perf_counter()-a)*1000/repeats
        return {'mongo_avg_ms':round(mongo_avg,3),'first_query_ms':round(cold,3),'cached_avg_ms':round(warm,3),'repeats':repeats}
