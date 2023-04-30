from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import SearchForm, PublisherForm
from .models import Book, Contributor, Publisher
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


def form_example(request):
    return render(request, "form-example.html")


def book_search(request):
    search_text = request.GET.get('search', "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid() and form.cleaned_data['search']:
        search = form.cleaned_data['search']
        search_in = form.cleaned_data.get('search_in') or "title"
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        if search_in == "title":
            books = Book.objects.filter(title__icontains=search)
        else:
            fname_contributors = Contributor.objects.filter(first_names__icontains=search)

            for contributor in fname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

            lname_contributors = Contributor.objects.filter(last_names__icontains=search)

            for contributor in lname_contributors:
                for book in contributor.book_set.all():
                    books.add(book)

    return render(request, "search-result.html", {'search_text': search_text, 'form': form, 'books': books})

def book_detail(request,pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            'book': book,
            'book_rating': book_rating,
            'number_of_reviews': reviews}
    else:
        context = {
            'book': book,
            'book_rating': None,
            'number_of_reviews': None}

    return render(request, "book_detail.html", context)

def publisher_edit(request, pk=None):
    if pk is None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            update_publisher = form.save()
            if publisher is None:
                messages.success(request, "Dodano nowego wydawcę.")
            else:
                messages.success(request, "Zaktualizowano dane wydawcy = {}".format(update_publisher.name))
            return redirect("publisher_edit",update_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "form-example.html", {"form": form, "method": request.method, "publisher": publisher, "pk": pk})
