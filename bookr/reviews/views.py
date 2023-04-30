from io import BytesIO

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.images import ImageFile
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from .models import Book, Contributor, Publisher, Review
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


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {
            'book': book,
            'book_rating': book_rating,
            'reviews': reviews}
    else:
        context = {
            'book': book,
            'book_rating': None,
            'reviews': None}

    return render(request, "book_detail.html", context)


def publisher_edit(request, pk=None):
    if pk is not None:
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
            return redirect("publisher_edit", update_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)

    return render(request, "form-example.html",
                  {"form": form, "publisher": publisher, "model_type": "Publisher"})

@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)

    if review_pk is not None:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            update_review = form.save(False)
            update_review.book = book

            if review is None:
                messages.success(request, "Dodano nową recenzję.")
            else:
                update_review.date_edited = timezone.now()
                messages.success(request, "Zaktualizowano dane recenzji = {}".format(book.title))

            update_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, "instance-form.html",
                  {"form": form,
                   "instance": review,
                   "model_type": "Review",
                   "related_instance": book,
                   "related_model_type": "Book",
                   })

@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookMediaForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            book = form.save(False)

            cover = form.cleaned_data.get('cover')

            if cover and not hasattr(cover, "path"):
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            messages.success(request, "Zaktualizowano okładkę książki = {}".format(book.title))
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)

    return render(request, "instance-form.html",
                  {"form": form, "instance": book, "model_type": "Book", "is_file_upload": True})
