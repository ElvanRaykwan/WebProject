from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("nonactive", views.non, name="non"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watch", views.watch, name="watch"),
    path("new", views.new, name="new"),
    path("category", views.category, name="category"),
    path("category/<str:cat_type>", views.cat_type, name="category_link"),
    path("item/<str:item_id>", views.item, name="item")
]
