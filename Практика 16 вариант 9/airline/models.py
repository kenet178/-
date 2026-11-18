from django.db import models
from django.core.exceptions import ValidationError
class Airport(models.Model):
    code=models.CharField(max_length=8,unique=True,verbose_name='Код')
    city=models.CharField(max_length=100,verbose_name='Город')
    def __str__(self):return f'{self.city} ({self.code})'
class Aircraft(models.Model):
    model=models.CharField(max_length=100,unique=True)
    capacity=models.PositiveIntegerField(default=100)
    def __str__(self):return self.model
class Passenger(models.Model):
    full_name=models.CharField(max_length=120)
    email=models.EmailField(unique=True)
    def __str__(self):return self.full_name
class Flight(models.Model):
    class Status(models.TextChoices):
        SCHEDULED='scheduled','По расписанию'
        DELAYED='delayed','Задержан'
        CANCELLED='cancelled','Отменён'
    number=models.CharField(max_length=20,unique=True,verbose_name='Номер рейса')
    origin=models.ForeignKey(Airport,related_name='outbound_flights',on_delete=models.PROTECT,verbose_name='Откуда')
    destination=models.ForeignKey(Airport,related_name='inbound_flights',on_delete=models.PROTECT,verbose_name='Куда')
    aircraft=models.ForeignKey(Aircraft,on_delete=models.PROTECT,verbose_name='Самолёт')
    departure=models.DateTimeField(verbose_name='Отправление')
    price=models.DecimalField(max_digits=10,decimal_places=2,verbose_name='Стоимость')
    status=models.CharField(max_length=20,choices=Status.choices,default=Status.SCHEDULED)
    passengers=models.ManyToManyField(Passenger,through='Ticket',related_name='flights')
    class Meta:
        ordering=['departure'];indexes=[models.Index(fields=['departure','status'],name='flight_departure_idx')]
    def clean(self):
        if self.origin_id and self.origin_id==self.destination_id:
            raise ValidationError({'destination':'Аэропорты должны отличаться'})
        if self.price is not None and self.price<=0:
            raise ValidationError({'price':'Цена должна быть положительной'})
    def __str__(self):return self.number
class Ticket(models.Model):
    flight=models.ForeignKey(Flight,on_delete=models.CASCADE,related_name='tickets')
    passenger=models.ForeignKey(Passenger,on_delete=models.PROTECT,related_name='tickets')
    seat=models.PositiveSmallIntegerField()
    class Meta:
        constraints=[models.UniqueConstraint(fields=['flight','seat'],name='unique_flight_seat'),
                     models.UniqueConstraint(fields=['flight','passenger'],name='unique_flight_passenger')]
    def clean(self):
        if self.flight_id and self.seat>self.flight.aircraft.capacity:
            raise ValidationError({'seat':'Место больше вместимости самолёта'})
    def __str__(self):return f'{self.flight.number}: {self.seat}'
