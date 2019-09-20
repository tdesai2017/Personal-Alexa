from django.urls import path
from myapp import views



app_name = 'myapp'

urlpatterns = [
# /home
path('', views.home, name = 'home'),

path('shopping_list', views.shopping_list, name = 'shopping_list'),
path('receive_shopping_list_add/', views.receive_shopping_list_add, name = 'receive_shopping_list_add'),
path('receive_shopping_list_delete/', views.receive_shopping_list_delete, name = 'receive_shopping_list_delete'),
path('receive_shopping_list_clear/', views.receive_shopping_list_clear, name = 'receive_shopping_list_clear'),
path('read_shopping_list/', views.read_shopping_list, name = 'read_shopping_list'),



path('reminders', views.reminders, name = 'reminders'),
path('receive_reminders_add/', views.receive_reminders_add, name = 'receive_reminders_add'),
path('receive_reminders_delete/', views.receive_reminders_delete, name = 'receive_reminders_delete'),
path('receive_reminders_clear/', views.receive_reminders_clear, name = 'receive_reminders_clear'),
path('read_reminders/', views.read_reminders, name = 'read_reminders_'),



   
  
]