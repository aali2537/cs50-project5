
from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_post, name="allpost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("newpost", views.new_post, name="newPost"),
    path("allpost", views.all_post, name="allPost"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    #Api Routes
    path("likes/<int:post_id>", views.like, name="like"),
    path("follow/<str:owner>", views.follow, name="follow")
]
