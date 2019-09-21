from django.shortcuts import render          
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request,'spotify/index.html')   # this is the route/link index.html  


# def about(request):   -- in case you want to add another page to the website..
#      return render(request,'spotify/about.html')

