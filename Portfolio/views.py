from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def info(request):
    return render(request, 'Portfolio/index.html')