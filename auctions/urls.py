from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:auction_id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:auction_id>", views.watchlist_remove, name="watchlist_remove"),
    path("bid", views.bid, name="bid"),
    path("<int:listing_id>/close", views.close, name="close"),
    path("<int:listing_id>/auction_comments", views.auction_comments, name="auction_comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.categories_choose, name="categories_choose"),
]
