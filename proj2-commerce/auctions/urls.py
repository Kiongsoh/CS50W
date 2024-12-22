from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:post_id>", views.listing, name="listing"),
    path("addWatchlist/<int:post_id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:post_id>", views.removeWatchlist, name="removeWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new_bid/<int:post_id>", views.new_bid, name="new_bid"),
    path("close_bid/<int:post_id>", views.close_bid, name="close_bid"),
    path("comment/<int:post_id>", views.comment, name="comment"),
    ]


# refer to wiki urls.py
# user id to get unique url path
# active listing, listing and categories