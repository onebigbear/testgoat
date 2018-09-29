from django.shortcuts import render, redirect

from .models import Item
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		new_item_text = request.POST['item_text']
		Item.objects.create(text=new_item_text)
		return redirect('/lists/')
	items = Item.objects.all()
	
	return render(request, 'lists/home.html', {'items':items})


