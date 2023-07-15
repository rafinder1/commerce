from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "photos": Photo.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def getLastPk(obj):
    if (obj.objects.first() is None):
        return 1
    else:
        get_pk = obj.objects.order_by('-pk')[0]
        last_pk = get_pk.pk + 1
        return last_pk


def create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        date = datetime.now()
        category_obj = Category.objects.get(pk=category_id)

        new_auction = Auction(id=getLastPk(Auction), name=name, current_bid=price, description=description,
                              creation_date=date, auction_category=category_obj, available=True, creator=request.user)
        new_auction.save()

        if request.FILES.get('img', False):
            img = request.FILES['img']
            fs = FileSystemStorage()
            name = fs.save(img.name, img)
            url = fs.url(name)
            photo = Photo(getLastPk(Photo), img.name, url)
            photo.save()

            new_auction.photos.add(photo)
            new_auction.save()

        return redirect('index')
    return render(request, "auctions/create.html", {
        "categories": Category.objects.all(),
    })


def listing(request, listing_id):
    listing = Auction.objects.get(pk=listing_id)
    comments = Comment.objects.filter(auction=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "photos": Photo.objects.all(),
        "comments": comments
    })


def watchlist_add(request, auction_id):
    if request.user.is_authenticated:

        if WatchList.objects.filter(user=request.user).exists():
            watchlist = WatchList.objects.get(user=request.user)
        else:
            watchlist = WatchList(id=getLastPk(WatchList), user=request.user)

        auction_to_save = Auction.objects.get(id=auction_id)
        watchlist.save()
        watchlist.auctions.add(auction_to_save)
        watchlist.save()

    return render(request, "auctions/watchlist.html", {
        "watch_list": watchlist.auctions.all(),
    })


def watchlist_remove(request, auction_id):
    if request.user.is_authenticated:
        return redirect('index')


def bid(request):
    message = ""
    if request.method == "POST":
        if request.user.is_authenticated:
            price = int(request.POST.get('bid'))
            auction_id = request.POST.get('auction_id')

            auction = Auction.objects.get(pk=auction_id)
            current_bid = auction.current_bid

            if (price > current_bid):
                auction.current_bid = price
                auction.save()

                new_bid = Bid(id=getLastPk(Bid), amount=price, auction=auction, bidder=request.user)
                new_bid.save()

                messages.add_message(request, messages.INFO, f"Success - bid for {price}")

            else:
                messages.add_message(request, messages.INFO, f"Your must add more then {current_bid}")
        else:
            messages.add_message(request, messages.INFO, "you are not authenticated")

    return redirect('index')


def close(request, listing_id):
    auction = Auction.objects.get(pk=listing_id)
    bids = Bid.objects.filter(auction=auction)
    max_price = bids.order_by('-amount')[0]

    winner = max_price.bidder
    auction.winner = winner
    auction.available = False
    auction.save()

    return render(request, "auctions/close.html", {
        "max_price": max_price.amount,
        "winner": winner
    })


def auction_comments(request, listing_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            listing = Auction.objects.get(pk=listing_id)
            text = request.POST['text']
            com = Comment(id=getLastPk(Comment), commenter=request.user, auction=listing, text=text)
            com.save()
            return redirect('listing', listing_id=listing_id)


def watchlist(request):
    watchlist = WatchList.objects.get(user=request.user)

    return render(request, "auctions/watchlist.html", {
        "watch_list": watchlist.auctions.all(),
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })


def categories_choose(request, category_id):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(auction_category=category_id),
        "photos": Photo.objects.all(),
    })
