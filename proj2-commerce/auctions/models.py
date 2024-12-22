from django.contrib.auth.models import AbstractUser
from django.db import models


# USE CAPITALISE FOR FIRST LETTER IN NAME
class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    # display category name in admin panel
    def __str__(self):
        return self.categoryName

# list of all items listed
class Listing(models.Model):
    # see Django doc to see all data types that exists
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    start_bid = models.FloatField()
    image_url = models.CharField(max_length=500)
    active_status = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='userlist')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='category') 
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listingwatchlist")

    # display item name in admin panel
    def __str__(self):
        return self.title

# table of all bidding transactions, with 1st entry being the listed price
class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='bidder_name')
    price = models.FloatField()
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE, related_name='auction_item')
    date_time = models.DateTimeField(auto_now_add=True)

    # display item name in admin panel
    def __str__(self):
        return f'{self.listing.title} {self.price}'
    
# table of all comments
class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='author_name')
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    # display item name in admin panel
    def __str__(self):
        return f'{self.author} {self.listing.title}'