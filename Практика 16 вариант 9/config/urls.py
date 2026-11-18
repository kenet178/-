from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from airline import views
urlpatterns=[
 path('admin/',admin.site.urls),
 path('accounts/login/',auth_views.LoginView.as_view(template_name='registration/login.html'),name='login'),
 path('accounts/logout/',auth_views.LogoutView.as_view(),name='logout'),
 path('',views.home,name='home'),
 path('flights/',views.flight_list,name='flights'),
 path('flights/new/',views.flight_create,name='flight_create'),
 path('flights/<int:pk>/',views.flight_detail,name='flight_detail'),
 path('flights/<int:pk>/edit/',views.flight_edit,name='flight_edit'),
 path('flights/<int:pk>/delete/',views.flight_delete,name='flight_delete'),
 path('flights/<int:pk>/book/',views.book_ticket,name='book_ticket'),
 path('statistics/',views.statistics,name='statistics')]
