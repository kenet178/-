from django.contrib import admin
from .models import Airport,Aircraft,Flight,Passenger,Ticket
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display=['number','origin','destination','departure','status','price']
    search_fields=['number','origin__city','destination__city']
    list_filter=['status','origin','destination']
    list_select_related=['origin','destination','aircraft']
admin.site.register([Airport,Aircraft,Passenger,Ticket])
