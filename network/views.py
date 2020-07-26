from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required(login_url= "/login")
def new_post(request):
    # Handle user creating a new post
    if request.method == "POST":
        # Grab user post information
        print("does this hit?")
        poster = request.user.get_username()
        content = request.POST["content"]
        time = datetime.now()

        # Update database with new post
        Post.objects.create(poster = poster, content = content, time = time)

        return HttpResponseRedirect(reverse("index"))

    #Else show user new post creation page    
    return render(request, "network/newpost.html")

def all_post(request):
    # Grab all posts from database to pass to template
    postList = Post.objects.all()
    
    #Order posts by time and serialize time object
    postList = postList.order_by("-time").all()
    postList = [post.serialize for post in postList]

    return render(request, "network/allpost.html", {
        "postList": postList,
        "currentUser": request.user.get_username()
    })

@login_required
def like(request, post_id):
    #Grab current user object and post obj from database
    userObj = User.objects.get(username=request.user)
    try:
        postObj = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    #Check to see if user has liked post or not already
    if postObj.liked.filter(username=request.user).exists():
       #User has already liked so remove and update count
       postObj.liked.remove(userObj)
       postObj.likes = postObj.likes - 1
    else:
       #User has not liked yet so add one like
       postObj.liked.add(userObj)
       postObj.likes = postObj.likes + 1

    postObj.save()
    return JsonResponse({"likes": postObj.likes})