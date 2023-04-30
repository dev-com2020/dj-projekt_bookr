import django
from django.contrib import admin

from django.urls import path, include
from . import views


# importujemy nasz moduł reviews.views PyCharm zawsze podkreśla nam to na czerwono, ale nie przejmuj się tym

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('books/', views.book_list, name='book_list'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
    path('book-search/', views.book_search, name='book_search'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/media', views.book_media, name='book_media'),
    path('books/<int:book_pk>/review/new/', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/review/<int:review_pk>/', views.review_edit, name='review_edit'),
]