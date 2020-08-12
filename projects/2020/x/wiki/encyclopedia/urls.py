from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('/search', views.search, name="search"),
    path('/new', views.new, name="new_page"),
    path('/random', views.random_view, name="random"),
    path('/<str:entry_name>', views.entry, name="entry"),
    path('/<str:entry_name>/edit', views.edit, name="edit"),
]
