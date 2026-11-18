from django import forms
from .models import Flight,Ticket
class FlightForm(forms.ModelForm):
    class Meta:
        model=Flight
        fields=['number','origin','destination','aircraft','departure','price','status']
        widgets={'departure':forms.DateTimeInput(attrs={'type':'datetime-local'},format='%Y-%m-%dT%H:%M')}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['departure'].input_formats=['%Y-%m-%dT%H:%M','%Y-%m-%d %H:%M:%S']
class TicketForm(forms.Form):
    full_name=forms.CharField(max_length=120,label='ФИО')
    email=forms.EmailField(label='Email')
    seat=forms.IntegerField(min_value=1,label='Место')
