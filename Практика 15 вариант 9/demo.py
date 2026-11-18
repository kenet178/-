from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Station, Train, Ticket
from app.services import TrainService, DomainError
from app.repositories import TrainRepository


def main():
    print('=== ПРАКТИКА 15. ВАРИАНТ 9: Ж/Д / FLASK ===')
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    with Session() as db:
        db.add_all([Station(name='Москва'), Station(name='Казань')]); db.commit()
        service = TrainService(db)
        train = service.save({'number':'РЖД-777','origin_id':1,'destination_id':2,
            'departure':'2026-12-20T12:00','fare':4000,'seats':50,'status':'scheduled'})
        print('CREATE:',train.id,train.number)
        print('LIST:',[(t.id,t.number) for t in TrainRepository(db).list(q='РЖД')])
        ticket = service.purchase(train.id,'Иван Петров',3)
        print('TICKET:',ticket.id,ticket.seat)
        try: service.purchase(train.id,'Другой пассажир',3)
        except DomainError as exc:print('DUPLICATE:',exc)
        print('REMAINING SEATS:',TrainRepository(db).get(train.id).seats)
    print('Для веб-интерфейса: python run.py')
    print('Демонстрация завершена успешно.')

if __name__ == '__main__': main()
