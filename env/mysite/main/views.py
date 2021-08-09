from django.shortcuts import render
from .models import Product #import Product from models

# Create your views here.
def homepage(request):
	product = Product.objects.all()[:4] #queryset containing all products we just created
	return render(request=request, template_name="main/home.html", context={'product':product})