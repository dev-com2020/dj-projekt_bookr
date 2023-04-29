from django.http import HttpResponse
from django.shortcuts import render

from .models import Book
from .utils import average_rating


# Create your views here.
def index(request):
    name = "Bookr"
    return render(request, "base.html", {"name": name})

def welcome_view(request):
    message = f"<html><h1>Welcome to Bookr!</h1></html> " \
              f"<p>{Book.objects.count()} książek w bazie danych</p></html>"
    return HttpResponse(message)

def book_list(request):
    global context
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({
            'book': book,
            'book_rating': book_rating,
            'number_of_reviews': number_of_reviews})
        context = {'book_list': book_list}
    return render(request, "book_list.html", context)














