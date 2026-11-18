import os
from sqlalchemy import create_engine,event
from sqlalchemy.orm import DeclarativeBase,sessionmaker
class Base(DeclarativeBase):pass
def make_engine():
    url=os.getenv('DATABASE_URL','sqlite:///./flights.db')
    args={'connect_args':{'check_same_thread':False}} if url.startswith('sqlite') else {}
    engine=create_engine(url,**args)
    if engine.dialect.name=='sqlite':
        @event.listens_for(engine,'connect')
        def fk(c,_):c.execute('PRAGMA foreign_keys=ON')
    return engine
engine=make_engine();SessionLocal=sessionmaker(engine,expire_on_commit=False)
def get_db():
    with SessionLocal() as db:yield db
