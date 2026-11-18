from django.db import transaction,IntegrityError
from django.db.models import Q,Count,Avg,Sum,Prefetch
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from .models import Flight,Airport,Aircraft,Passenger,Ticket
from .forms import FlightForm,TicketForm

def home(request):
    return render(request,'airline/home.html',{'total':Flight.objects.count(),
          'booked':Ticket.objects.count()})
def flight_list(request):
    qs=Flight.objects.select_related('origin','destination','aircraft')
    q=request.GET.get('q','').strip()
    if q:qs=qs.filter(Q(number__icontains=q)|Q(origin__city__icontains=q)|Q(destination__city__icontains=q))
    if request.GET.get('status'):qs=qs.filter(status=request.GET['status'])
    origin = request.GET.get('origin', '')
    if origin.isdecimal() and len(origin) <= 18:
        qs = qs.filter(origin_id=int(origin))
    sort=request.GET.get('sort','departure')
    if sort not in ('departure','price','number','-price','-departure','-number'):sort='departure'
    page=Paginator(qs.order_by(sort),6).get_page(request.GET.get('page'))
    return render(request,'airline/list.html',{'page_obj':page,'airports':Airport.objects.all(),
       'statuses':Flight.Status.choices,'q':q,'sort':sort})
def flight_detail(request,pk):
    flight=get_object_or_404(Flight.objects.select_related('origin','destination','aircraft').prefetch_related('tickets__passenger'),pk=pk)
    return render(request,'airline/detail.html',{'flight':flight,'form':TicketForm()})
@login_required
def flight_create(request):
    form=FlightForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        flight=form.save();messages.success(request,'Рейс создан');return redirect('flight_detail',pk=flight.pk)
    return render(request,'airline/form.html',{'form':form,'title':'Новый рейс'})
@login_required
def flight_edit(request,pk):
    if not request.user.is_staff:return HttpResponseForbidden('Редактировать может только персонал')
    flight=get_object_or_404(Flight,pk=pk)
    form=FlightForm(request.POST or None,instance=flight)
    if request.method=='POST' and form.is_valid():
        form.save();messages.success(request,'Рейс обновлён');return redirect('flight_detail',pk=pk)
    return render(request,'airline/form.html',{'form':form,'title':'Редактирование рейса'})
@login_required
@require_POST
def flight_delete(request,pk):
    if not request.user.is_staff:return HttpResponseForbidden('Удалять может только персонал')
    flight=get_object_or_404(Flight,pk=pk)
    flight.delete();messages.success(request,'Рейс удалён');return redirect('flights')
@login_required
@require_POST
def book_ticket(request,pk):
    flight=get_object_or_404(Flight.objects.select_related('aircraft'),pk=pk)
    form=TicketForm(request.POST)
    if not form.is_valid():messages.error(request,'Проверьте данные билета');return redirect('flight_detail',pk=pk)
    if flight.status==Flight.Status.CANCELLED:
        messages.error(request,'Рейс отменён');return redirect('flight_detail',pk=pk)
    if form.cleaned_data['seat']>flight.aircraft.capacity:
        messages.error(request,'Место выходит за пределы самолёта');return redirect('flight_detail',pk=pk)
    try:
        with transaction.atomic():
            passenger,_=Passenger.objects.get_or_create(email=form.cleaned_data['email'],
                       defaults={'full_name':form.cleaned_data['full_name']})
            Ticket.objects.create(flight=flight,passenger=passenger,seat=form.cleaned_data['seat'])
        messages.success(request,'Билет успешно приобретён')
    except IntegrityError:
        messages.error(request,'Место занято или пассажир уже зарегистрирован на рейс')
    return redirect('flight_detail',pk=pk)
def statistics(request):
    stats=Flight.objects.aggregate(count=Count('id'),avg=Avg('price'))
    summary={'flights':stats['count'],'average_price':stats['avg'],
             'airports':Airport.objects.count(),'passengers':Passenger.objects.count(),
             'tickets':Ticket.objects.count(),'aircraft':Aircraft.objects.count(),
             'by_status':list(Flight.objects.values('status').annotate(cnt=Count('id')).order_by('status'))}
    return render(request,'airline/stats.html',{'stats':summary})
