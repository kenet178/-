import django.db.models.deletion
from django.db import migrations,models
class Migration(migrations.Migration):
    initial=True
    dependencies=[]
    operations=[
        migrations.CreateModel(name='Airport',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),
            ('code',models.CharField(max_length=8,unique=True,verbose_name='Код')),
            ('city',models.CharField(max_length=100,verbose_name='Город'))]),
        migrations.CreateModel(name='Aircraft',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),
            ('model',models.CharField(max_length=100,unique=True)),('capacity',models.PositiveIntegerField(default=100))]),
        migrations.CreateModel(name='Passenger',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),
            ('full_name',models.CharField(max_length=120)),('email',models.EmailField(max_length=254,unique=True))]),
        migrations.CreateModel(name='Flight',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),
            ('number',models.CharField(max_length=20,unique=True,verbose_name='Номер рейса')),
            ('departure',models.DateTimeField(verbose_name='Отправление')),
            ('price',models.DecimalField(decimal_places=2,max_digits=10,verbose_name='Стоимость')),
            ('status',models.CharField(choices=[('scheduled','По расписанию'),('delayed','Задержан'),('cancelled','Отменён')],default='scheduled',max_length=20)),
            ('aircraft',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,to='airline.aircraft',verbose_name='Самолёт')),
            ('destination',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='inbound_flights',to='airline.airport',verbose_name='Куда')),
            ('origin',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='outbound_flights',to='airline.airport',verbose_name='Откуда'))],
            options={'ordering':['departure']}),
        migrations.CreateModel(name='Ticket',fields=[('id',models.BigAutoField(primary_key=True,serialize=False)),
            ('seat',models.PositiveSmallIntegerField()),
            ('flight',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='tickets',to='airline.flight')),
            ('passenger',models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,related_name='tickets',to='airline.passenger'))]),
        migrations.AddField(model_name='flight',name='passengers',field=models.ManyToManyField(related_name='flights',through='airline.Ticket',to='airline.passenger')),
        migrations.AddConstraint(model_name='ticket',constraint=models.UniqueConstraint(fields=('flight','seat'),name='unique_flight_seat')),
        migrations.AddConstraint(model_name='ticket',constraint=models.UniqueConstraint(fields=('flight','passenger'),name='unique_flight_passenger')),
        migrations.AddIndex(model_name='flight',index=models.Index(fields=['departure','status'],name='flight_departure_idx')),
    ]
