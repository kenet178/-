import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


def main():
    import django
    django.setup()
    from django.core.management import call_command
    from django.test import Client
    from django.contrib.auth import get_user_model
    from airline.models import Flight,Airport,Aircraft,Passenger,Ticket
    call_command('migrate', verbosity=0)
    call_command('seed_airline', verbosity=0)
    client=Client()
    print('=== ПРАКТИКА 16. ВАРИАНТ 9: DJANGO / АВИАКОМПАНИЯ ===')
    print('HOME:',client.get('/').status_code)
    print('LIST:',client.get('/flights/').status_code)
    print('STATISTICS:',client.get('/statistics/').status_code)
    print('FLIGHTS:',list(Flight.objects.values_list('number','status')[:5]))
    print('AIRPORTS:',list(Airport.objects.values_list('code','city')[:5]))
    print('AIRCRAFT:',list(Aircraft.objects.values_list('model','capacity')[:5]))
    print('PASSENGERS:',Passenger.objects.count(),'TICKETS:',Ticket.objects.count())
    flight=Flight.objects.first()
    if flight:print('DETAIL:',client.get(f'/flights/{flight.pk}/').status_code)
    print('Демонстрация завершена успешно.')

if __name__=='__main__':main()
