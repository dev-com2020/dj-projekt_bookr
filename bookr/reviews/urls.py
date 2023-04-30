import django
from django.contrib import admin

from django.urls import path, include
from . import views
from bookr import settings

# importujemy nasz moduł reviews.views PyCharm zawsze podkreśla nam to na czerwono, ale nie przejmuj się tym

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('books/', views.book_list, name='book_list'),
    # path('form/', views.form_example, name='form_example'),
    path('book-search/', views.book_search, name='book_search'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),

]