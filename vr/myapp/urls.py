from django.urls import path
from myapp import views



app_name = 'myapp'

urlpatterns = [
# /home
path('', views.home, name = 'home'), 

path('receive_add/', views.receive_add, name = 'receive_add'),
path('receive_delete/', views.receive_delete, name = 'receive_delete'),
path('receive_clear/', views.receive_clear, name = 'receive_clear'),
path('read_shopping_list/', views.read_shopping_list, name = 'read_shopping_list'),



   
  
]