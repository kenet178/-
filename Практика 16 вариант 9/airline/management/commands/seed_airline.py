from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from airline.models import Airport,Aircraft,Flight,Passenger,Ticket
class Command(BaseCommand):
    help='Создать 20+ учебных записей для варианта 9'
    def handle(self,*args,**kwargs):
        codes=[('SVO','Москва'),('LED','Санкт-Петербург'),('KZN','Казань'),('AER','Сочи'),('SVX','Екатеринбург')]
        airports=[Airport.objects.get_or_create(code=code,defaults={'city':city})[0] for code,city in codes]
        aircraft=Aircraft.objects.get_or_create(model='Airbus A320',defaults={'capacity':150})[0]
        base=timezone.now()+timedelta(days=30)
        for i in range(20):
            Flight.objects.get_or_create(number=f'SU{i+100}',defaults={'origin':airports[i%5],
               'destination':airports[(i+1)%5],'aircraft':aircraft,'departure':base+timedelta(days=i),
               'price':Decimal('5900')+Decimal(i*150),'status':'scheduled' if i%4 else 'delayed'})
        for i in range(5):
            p,_=Passenger.objects.get_or_create(email=f'pass{i}@example.org',defaults={'full_name':f'Тестовый пассажир {i}'})
            flight=Flight.objects.get(number=f'SU{100+i}')
            Ticket.objects.get_or_create(flight=flight,passenger=p,defaults={'seat':i+1})
        self.stdout.write(self.style.SUCCESS(f'Создано/проверено рейсов: {Flight.objects.count()}'))
