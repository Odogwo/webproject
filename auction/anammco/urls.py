from django.urls import path

from . import views

# anammco/urls.py
from .views import auction_list, place_bid

urlpatterns = [
    path("", views.index, name="index"),
    path('auction-list/', auction_list, name='auction_list'),
    path('place-bid/<int:item_id>/', place_bid, name='place_bid'),
    # Add more paths as needed for your app
]