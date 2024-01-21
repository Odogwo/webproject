from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Item, Bid
from django.http import HttpResponse


def index(request):
    return render(request, 'anammco/index.html')



@login_required
def auction_list(request):
    items = Item.objects.filter(auction_end_time__gte=timezone.now())
    return render(request, 'auction/auction_list.html', {'items': items})

@login_required
def place_bid(request, item_id):
    item = Item.objects.get(pk=item_id)
    if request.method == 'POST':
        bid_amount = request.POST['bid_amount']
        if float(bid_amount) > item.current_bid:
            Bid.objects.create(bidder=request.user, item=item, bid_amount=bid_amount)
            item.current_bid = bid_amount
            item.save()
    return redirect('auction_list')
