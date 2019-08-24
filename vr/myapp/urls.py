from django.urls import path
from myapp import views


app_name = 'myapp'

urlpatterns = [

path('', views.home, name = 'home'),
path('receive_add/', views.receive_add, name = 'receive_add'),

   
  
]