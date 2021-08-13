from django.urls import path
from django.contrib import admin
from . import views

   
app_name = 'reviews'

urlpatterns = [
    path("", views.welcome_view, name="welcome_view"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name='book_detail')


    ]




