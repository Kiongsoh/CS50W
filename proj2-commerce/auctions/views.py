from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

# default route to view all active listings
def index(request):
    try:
        # retreive all active items listed from [Listing] table
        active_listing = Listing.objects.filter(active_status=True)
        # retrieve all categories defined in table
        food_category = Category.objects.all()

        # how to display last price of all active listings?
        last_bid_dict = {}

        for listing in active_listing:
            # retreive all bids history for 1 listing
            all_bids = Bid.objects.filter(listing=listing)
            last_bid = all_bids.last()
            last_bid_dict[listing.id]=last_bid.price

    except Listing.DoesNotExist:
        active_listing = None

    print(last_bid.price)
    return render(request, "auctions/index.html",
        {"active_listing": active_listing,
         'food_category': food_category,
         'all_last_bids': last_bid_dict

         })

# handles the drop down category filter to render index page with selected category
def displayCategory(request):
    if request.method == "POST":
        # retrieve all categories defined in table
        food_category = Category.objects.all()

        # get category submitted on form
        category_from_form = request.POST['category']

        # if all is selected
        if category_from_form == "All Categories":
            selected_listings = Listing.objects.filter(active_status=True)
        
        # if one category is selected
        else:
            # use submitted string to find category class in table
            selected_category = Category.objects.get(categoryName = category_from_form)
            # category in Listing is defined as a Foreign key
            selected_listings = Listing.objects.filter(active_status=True, category=selected_category)

        return render(request, "auctions/index.html",
            {"active_listing": selected_listings,
            'food_category': food_category})

# replcia of displayCategory, but renders for watchlist page instead of index
def watchlist(request):
    food_category = Category.objects.all()
    current_user = request.user
    watchlist_listings = current_user.listingwatchlist.all()
    
    if request.method == "GET":
        # listingwatchlist is a related name of watchlist in Listing()
        return render(request, "auctions/watchlist.html",
            {"active_listing": watchlist_listings,
            'food_category': food_category})
    else: 
        # get category submitted on form
        category_from_form = request.POST['category']

        # if all is selected
        if category_from_form == "All Categories":
            selected_listings = watchlist_listings
        
        # if one category is selected
        else:
            selected_category = Category.objects.get(categoryName = category_from_form)
            # category in Listing is defined as a Foreign key
            selected_listings = watchlist_listings.filter(active_status=True, category=selected_category)

        return render(request, "auctions/watchlist.html",
            {"active_listing": selected_listings,
            'food_category': food_category})


# display individual listing details, including last bid price
def listing(request, post_id, message=None):
    listingdata = Listing.objects.get(pk=post_id)
    # if current user is in the list of User stored in the listingdata.watchlist column
    is_watchlist = request.user in listingdata.watchlist.all()
    # get all bids related to a specific listing
    all_bids = Bid.objects.filter(listing=listingdata)
    # isolating the last bid. first() was introduced in notes
    last_bid = all_bids.last()

    # getting all comments
    all_commments = Comments.objects.filter(listing=listingdata)

    return render(request, "auctions/listing.html",
        {"listing": listingdata,
         "is_watchlist": is_watchlist,
         "last_bid": last_bid,
         "message": message,
         "all_commments": all_commments
         })

def comment(request, post_id):

    listingdata = Listing.objects.get(pk=post_id)
    comment_from_form = request.POST['user_comment']

    comment_new_row = Comments(
        author = request.user,
        comment = comment_from_form,
        listing = listingdata
    )
    # list_new_row.id to get unique id
    comment_new_row.save()
    
    return HttpResponseRedirect(reverse("listing", args=(post_id, )))


# user can bid for items
def new_bid(request, post_id):
    listingdata = Listing.objects.get(pk=post_id)
    all_bids = Bid.objects.filter(listing=listingdata)

    # using last() function to retreive data from many to many relattionships
    last_bid = all_bids.last().price

    # retrieve bid submission from form
    bid_from_form = float(request.POST['bid_price'])

    # check if bid submission is bigger than last bid
    if bid_from_form > last_bid:
        bid_new_row = Bid(
            bidder = request.user,
            price = bid_from_form,
            listing = listingdata
        )
        # list_new_row.id to get unique id
        bid_new_row.save()
        return HttpResponseRedirect(reverse("listing", args=(post_id, )))

    else:
        # if bid is lower, present an error
        message = "Bid price must be higher than last bid price"
        # render error page
        # return render(request, "auctions/error.html",
        #     {"message": message
        #     })

        listingdata = Listing.objects.get(pk=post_id)
        # if current user is in the list of User stored in the listingdata.watchlist column
        is_watchlist = request.user in listingdata.watchlist.all()
        # get all bids related to a specific listing
        all_bids = Bid.objects.filter(listing=listingdata)
        # isolating the last bid. first() was introduced in notes
        last_bid = all_bids.last()

        return render(request, "auctions/listing.html",
            {"listing": listingdata,
            "is_watchlist": is_watchlist,
            "last_bid": last_bid,
            "message": message,
            })
        

# owner can closes bid for his own item
def close_bid(request, post_id):
    current_user = request.user
    # update active status in listing
    row_to_update = Listing.objects.get(pk=post_id)
    row_to_update.active_status = False
    row_to_update.save()
    return HttpResponseRedirect(reverse("listing", args=(post_id, )))

# if user is signed in, user should be able to add or remove items from their watch list
# updating of many to many r/s, use add() or remove() of the column
# ----------------------------------------------------------------------
def addWatchlist(request, post_id):
    current_user = request.user
    row_to_update = Listing.objects.get(pk=post_id)
    row_to_update.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(post_id, )))

def removeWatchlist(request, post_id):
    current_user = request.user
    row_to_update = Listing.objects.get(pk=post_id)
    row_to_update.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(post_id, )))
# ----------------------------------------------------------------------

def create(request):
    if request.method == "GET":
        current_user = request.user
        print(current_user)
        # displays as object on webpage, not the category name
        food_category = Category.objects.all()
        return render(request, "auctions/create.html", 
            {'food_category': food_category})
    else:
        title = request.POST['title']
        description = request.POST['description']
        start_bid = request.POST['start_bid']
        image_url = request.POST['image_url']
        # category = request.POST['category'] will be just a string 
        # now category is a row object here
        category = Category.objects.get(categoryName = request.POST['category'])
        list_new_row = Listing(
            title = title,
            description = description,
            start_bid = start_bid,
            image_url = image_url,
            category = category,
            owner = request.user
        )
        # list_new_row.id to get unique id
        list_new_row.save()

        # create start bid as price in bid table
        bid_new_row = Bid(
            bidder = request.user,
            price = start_bid,
            listing = list_new_row
        )

        bid_new_row.save()
        return HttpResponseRedirect(reverse("index"))

        # return render(request, "index.html")
        # current_user = request.user


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

