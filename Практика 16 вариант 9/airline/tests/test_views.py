from decimal import Decimal
from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from airline.models import Airport,Aircraft,Passenger,Flight,Ticket

class ViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.a=Airport.objects.create(code='SVO',city='Москва')
        cls.b=Airport.objects.create(code='AER',city='Сочи')
        cls.c=Aircraft.objects.create(model='Airbus A320',capacity=100)
        cls.f=Flight.objects.create(number='SU101',origin=cls.a,destination=cls.b,
                  aircraft=cls.c,departure=timezone.now()+timedelta(days=1),price=Decimal('4500'))
        cls.user=User.objects.create_user('user',password='password123')
        cls.staff=User.objects.create_user('admin',password='password123',is_staff=True)
    def flight_payload(self,number='SU999'):
        return {'number':number,'origin':self.a.id,'destination':self.b.id,
                'aircraft':self.c.id,'departure':(timezone.now()+timedelta(days=2)).strftime('%Y-%m-%dT%H:%M'),
                'price':'5000','status':'scheduled'}
    def test_home(self):self.assertEqual(self.client.get('/').status_code,200)
    def test_list(self):self.assertEqual(self.client.get('/flights/').status_code,200)
    def test_detail(self):self.assertContains(self.client.get(f'/flights/{self.f.pk}/'),'SU101')
    def test_missing_detail(self):self.assertEqual(self.client.get('/flights/999/').status_code,404)
    def test_search(self):self.assertContains(self.client.get('/flights/?q=SU101'),'SU101')
    def test_search_empty(self):self.assertNotContains(self.client.get('/flights/?q=none'),'SU101')
    def test_filter(self):self.assertContains(self.client.get('/flights/?status=scheduled'),'SU101')
    def test_filter_empty(self):self.assertNotContains(self.client.get('/flights/?status=cancelled'),'SU101')
    def test_sort(self):self.assertEqual(self.client.get('/flights/?sort=-price').status_code,200)
    def test_pagination(self):
        for i in range(8):Flight.objects.create(number=f'SU{i+201}',origin=self.a,destination=self.b,aircraft=self.c,departure=timezone.now()+timedelta(days=i+1),price=4500)
        self.assertEqual(len(self.client.get('/flights/?page=1').context['page_obj']),6)
    def test_stats(self):self.assertContains(self.client.get('/statistics/'),'Средняя цена')
    def test_anonymous_create_redirect(self):self.assertEqual(self.client.get('/flights/new/').status_code,302)
    def test_login(self):self.assertTrue(self.client.login(username='user',password='password123'))
    def test_create_user(self):
        self.client.force_login(self.user);r=self.client.post('/flights/new/',self.flight_payload())
        self.assertEqual(r.status_code,302);self.assertTrue(Flight.objects.filter(number='SU999').exists())
    def test_create_validation(self):
        self.client.force_login(self.user);d=self.flight_payload();d['origin']=self.b.pk
        self.assertEqual(self.client.post('/flights/new/',d).status_code,200)
        self.assertFalse(Flight.objects.filter(number='SU999').exists())
    def test_user_cannot_edit(self):
        self.client.force_login(self.user);self.assertEqual(self.client.get(f'/flights/{self.f.pk}/edit/').status_code,403)
    def test_user_cannot_delete(self):
        self.client.force_login(self.user);self.assertEqual(self.client.post(f'/flights/{self.f.pk}/delete/').status_code,403)
    def test_staff_edit(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.post(f'/flights/{self.f.pk}/edit/',self.flight_payload('SU102')).status_code,302)
    def test_staff_delete(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.post(f'/flights/{self.f.pk}/delete/').status_code,302)
    def test_book(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.post(f'/flights/{self.f.pk}/book/',{'full_name':'Иван','email':'ivan@example.org','seat':7}).status_code,302)
        self.assertEqual(Ticket.objects.count(),1)
    def test_book_duplicate(self):
        self.client.force_login(self.user)
        data={'full_name':'Иван','email':'ivan@example.org','seat':7}
        self.client.post(f'/flights/{self.f.pk}/book/',data)
        self.client.post(f'/flights/{self.f.pk}/book/',data)
        self.assertEqual(Ticket.objects.count(),1)
    def test_admin_registered(self):
        self.client.force_login(self.staff);self.assertEqual(self.client.get('/admin/').status_code,200)
