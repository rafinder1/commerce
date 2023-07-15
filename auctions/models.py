from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)


class Photo(models.Model):
    image_name = models.TextField()
    url = models.TextField()


class Auction(models.Model):
    name = models.CharField(max_length=128)
    current_bid = models.IntegerField()
    creation_date = models.DateTimeField()
    available = models.BooleanField()
    description = models.CharField(max_length=128)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    photos = models.ManyToManyField(Photo, related_name='photos', blank=True)
    auction_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", default=1)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="creator", default=1)


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="auction")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    auctions = models.ManyToManyField(Auction, related_name="auctions", blank=True)
