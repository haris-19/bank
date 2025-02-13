from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('1',views.create, name = 'create'),
    path('2', views.pin, name= 'pin'),
    path('3', views.balance, name = 'balance'),
    path('4', views.deposit, name = 'deposit'),
    path('5', views.withdrawl, name = 'withdrawl'),
    path('6', views.acc_transfer, name = 'acc_transfer'),
]

