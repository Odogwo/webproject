from django.shortcuts import render, redirect #add this
from .models import Product #import Product from models
from django.core.paginator import Paginator #import Paginator
from .forms import NewUserForm #import NewUserForm from forms.py
from django.contrib.auth import login  #add this


# Create your views here.
def homepage(request):
	product = Product.objects.all()[:4] #queryset containing all products we just created
	return render(request=request, template_name="main/home.html", context={'product':product})


def products(request):
	products = Product.objects.all()
	paginator = Paginator(products, 2)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request = request, template_name="main/products.html", context = {"page_obj":page_obj})



def register(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("main:homepage")
	form = NewUserForm
	return render (request=request, template_name="main/register.html", context={"form":form})