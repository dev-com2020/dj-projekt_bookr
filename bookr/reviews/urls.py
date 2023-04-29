from django.contrib import admin
from django.urls import path, include
from . import views
# importujemy nasz moduł reviews.views PyCharm zawsze podkreśla nam to na czerwono, ale nie przejmuj się tym

urlpatterns = [
    path('', views.welcome_view, name='welcome'),

]