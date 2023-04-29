from django.http import HttpResponse
from django.shortcuts import render

from .models import Book


# Create your views here.
def index(request):
    name = "Bookr"
    return render(request, "base.html", {"name": name})

def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1></html> " \
              f"<p>{Book.objects.count()} książek w bazie danych</p></html>"
    return HttpResponse(message)
