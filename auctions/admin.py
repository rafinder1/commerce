from django.contrib import admin

from .models import Bid, Auction, Comment, Category, User, Photo


# Register your models here.
class AuctionAdmin(admin.ModelAdmin):
    list_display = (
        "name", "current_bid", "creation_date", "available", "winner", "auction_category", "creator"
    )


class BidAdmin(admin.ModelAdmin):
    list_display = (
        "auction", "bidder", "amount", "timestamp"
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "auction", "commenter", "text", "timestamp"
    )


admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Photo)
admin.site.register(User)
