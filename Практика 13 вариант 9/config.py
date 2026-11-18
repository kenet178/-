import os
MONGO_URL=os.getenv('MONGO_URL','mongodb://localhost:27017')
REDIS_URL=os.getenv('REDIS_URL','redis://localhost:6379/0')
MONGO_DB=os.getenv('MONGO_DB','airline_lab13')
