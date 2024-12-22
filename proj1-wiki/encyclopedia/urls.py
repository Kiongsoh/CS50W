from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("createpage", views.create_page, name="create_page"),
    # dynamic path, str:title is passed onto views.entry. url name is entry
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.rand, name="random")
]
