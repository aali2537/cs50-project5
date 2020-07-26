
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("newpost", views.new_post, name="newPost"),
    path("allpost", views.all_post, name="allPost"),
    path("register", views.register, name="register"),

    #Api Routes
    path("likes/<int:post_id>", views.like, name="like")
]
