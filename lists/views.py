from django.shortcuts import render
from .models import Item
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	item = Item()
	item.text = request.POST.get('item_text', '')
	item.save()
	return render(request, 'lists/home.html', {'new_item_text': item.text})

