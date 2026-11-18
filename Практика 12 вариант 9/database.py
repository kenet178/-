import os
from sqlalchemy import create_engine,event
from sqlalchemy.orm import DeclarativeBase,sessionmaker
class Base(DeclarativeBase):pass
def make_engine(url: str|None=None):
    engine=create_engine(url or os.getenv('DATABASE_URL','sqlite:///railway.db'),echo=False)
    if engine.dialect.name=='sqlite':
        @event.listens_for(engine,'connect')
        def fk(dbapi_conn,_):dbapi_conn.execute('PRAGMA foreign_keys=ON')
    return engine
engine=make_engine()
SessionLocal=sessionmaker(bind=engine,expire_on_commit=False)
def init(engine_to_init=None):
    import models
    Base.metadata.create_all(bind=engine_to_init or engine)
