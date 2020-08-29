from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Listing, Bids, Comments

import datetime



def index(request):
    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["description"]
        prc = request.POST["price"]
        url = request.POST["url"]
        cat = request.POST["category"]
        date = datetime.datetime.now()
        user = request.user
        new_list = Listing.objects.create(title=title, url=url, description=desc, price=prc, date=date, category=cat, user=user)
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/index.html", {
        "lists":Listing.objects.filter(active=True), "title":"Active Listing"
    })

def non(request):
    return render(request, "auctions/index.html", {
        "lists":Listing.objects.filter(active=False), "title":"Non-Active Listing"
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

def new (request):
    return render (request, "auctions/new.html")

def watch (request):
    return render (request, "auctions/watch.html",{
        'items':request.user.watchers.all()
    })


@login_required
def item (request, item_id):
    if request.method == "POST":
        if "submit_bid" in request.POST:
            try:
                bid = float(request.POST["new_bid"])
            except:
                messages.error(request, 'Error: Please only input numbers or decimals.')
                return HttpResponseRedirect(reverse("item",args={item_id:item_id}))
            highest = float(request.POST["highest"])
            item_id = request.POST["item_id"]
            item = Listing.objects.get(id=item_id)
            user = request.user

            if item.winner:
                messages.error(request, 'Error: The Auction is already over.')
                return HttpResponseRedirect(reverse("item",args={item_id:item_id}))

            if user == item.user:
                messages.error(request, 'Error: You are already the owner of this item.')
                return HttpResponseRedirect(reverse("item",args={item_id:item_id}))
            

            if highest == item.price:
                if highest == bid:
                    Bids.objects.create(user=user, bid=bid, item=item)
            
            if highest < bid:
                Bids.objects.create(user=user, bid=bid, item=item)
            else:
                if bid == item.price:
                    return HttpResponseRedirect(reverse("item",args={item_id:item_id}))
                else:
                    messages.error(request, 'Error: There is a higher bid or not enough for starting price. Please bid higher.')
                    return HttpResponseRedirect(reverse("item",args={item_id:item_id}))
            return HttpResponseRedirect(reverse("item", args={item_id:item_id}))
        
        elif "submit_comment" in request.POST:
            comment = request.POST["comment"]
            date = datetime.datetime.now()
            user = request.user
            item_id = request.POST["item_id"]
            item = Listing.objects.get(id = item_id)
            Comments.objects.create(content=comment, date_comment=date, user=user, item=item)
            return HttpResponseRedirect(reverse("item", args={item_id:item_id}))

        elif "watch" in request.POST:
            item_id = request.POST["item_id"]
            item = Listing.objects.get(id=item_id)
            state = request.POST["state"]
            if state == "Watch":
                item.watch_list.add(request.user)
            else:
                item.watch_list.remove(request.user)
            return HttpResponseRedirect(reverse("item", args={item_id:item_id}))

        elif "end" in request.POST:
            item_id = request.POST["item_id"]
            item = Listing.objects.get(id=item_id)
            winner = request.POST["winner"]
            try:
                item.winner = User.objects.get(username=winner)
                item.active = False
            except:
                messages.error(request, 'Error: No one has bid yet.')
                return HttpResponseRedirect(reverse("item",args={item_id:item_id}))
            item.save()
            return HttpResponseRedirect(reverse("item", args={item_id:item_id}))
            
    item = Listing.objects.get(id=item_id)
    bids = Bids.objects.filter(item=item)
    comments = Comments.objects.filter(item=item_id)
    bidders=[]
    number = Bids.objects.filter(item=item).count()
    price = item.price
    lead = "None"
    winner = False
    if item.winner:
        winner = True
    for bid in bids:
        if bid.bid >= price:
            price = bid.bid
            lead = bid.user
        if bid.user.username not in bidders:
            bidders.append(bid.user.username)
    user = request.user
    state = ""
    if user not in item.watch_list.all():
        state = "Watch"
    else:
        state = "Remove From Watch List"
    return render (request, "auctions/item.html",{
        "list":item, "bids":bids, "bidders": bidders, "number":number, "price":price, "lead":lead, "comments":comments,
        "state":state, "winner":winner
    })

def category(request):
    categories = ["No Category","Electronics","Fashion","Home","Toy"]
    return render (request, "auctions/category.html",{
        "categories":categories
    })

def cat_type(request, cat_type):
    return render (request, "auctions/cat_type.html",{
        "type": cat_type, "lists":Listing.objects.filter(category=cat_type)
    })
