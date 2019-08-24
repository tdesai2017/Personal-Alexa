from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from myapp.models import *

# Create your views here.

def home(request):
	context = Items.objects.all()
	return render(request, 'myapp/home.html', context)



def receive_add(request):
	if request.method=='POST':
		item = Item()
		item.name = request.Post['add']
		item.save()	
	return HttpResponseRedirect(reverse('myapp:home'))
