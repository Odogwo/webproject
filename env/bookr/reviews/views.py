from django.shortcuts import render

# Create your views here.




def index(request):
	name = "world"
	return render(request, "base.html", {"name": name})



