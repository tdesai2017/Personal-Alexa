from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from myapp.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def home(request):
	context = {'items':Item.objects.all()}
	return render(request, 'myapp/home.html', context)

@csrf_exempt 
def receive_add(request):
	if request.method=='POST':
		item_name = request.POST['add']
		if (Item.objects.filter(name = item_name)):
			messages.warning(request, 'There is already an input with the name "' + item_name + '"')
		else:
			item = Item()
			item.name = item_name.capitalize()
			item.save()	
	return HttpResponseRedirect(reverse('myapp:home'))


@csrf_exempt 
def receive_delete(request):
	if request.method=='POST':
		item_name = request.POST['delete'].capitalize()


		if (Item.objects.filter(name = item_name)):
			item_to_delete = Item.objects.get(name = item_name)
			item_to_delete.delete()

		else:
			messages.error(request, 'Sorry, there is no item with the name "' + item_name + '"')

		
	return HttpResponseRedirect(reverse('myapp:home'))


@csrf_exempt 
def receive_clear(request):
	if request.method=='POST':
		Item.objects.all().delete()
		
	return HttpResponseRedirect(reverse('myapp:home'))



@csrf_exempt 
def read_shopping_list(request):

	current_shopping_list = list(Item.objects.values('name'))
	print (current_shopping_list)
		
	return JsonResponse(current_shopping_list, safe = False)