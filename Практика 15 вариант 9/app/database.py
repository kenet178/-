from .config import Config
from sqlalchemy import create_engine,event
from sqlalchemy.orm import DeclarativeBase,sessionmaker
class Base(DeclarativeBase):pass
def configure(database_url=None):
    url=database_url or Config.DATABASE_URL
    args={'connect_args':{'check_same_thread':False}} if url.startswith('sqlite') else {}
    eng=create_engine(url,**args)
    if eng.dialect.name=='sqlite':
        @event.listens_for(eng,'connect')
        def _fk(c,_):c.execute('PRAGMA foreign_keys=ON')
    return eng,sessionmaker(eng,expire_on_commit=False)
