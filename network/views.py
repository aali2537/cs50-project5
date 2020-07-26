from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    return render(request, "network/allpost.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("allpost"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("allpost"))


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
        return HttpResponseRedirect(reverse("allpost"))
    else:
        return render(request, "network/register.html")

@login_required(login_url= "/login")
def new_post(request):
    # Handle user creating a new post
    if request.method == "POST":
        # Grab user post information
        poster = request.user.get_username()
        content = request.POST["content"]
        time = datetime.now()

        # Update database with new post
        Post.objects.create(poster = poster, content = content, time = time)

        return HttpResponseRedirect(reverse("allpost"))

    #Else show user new post creation page    
    return render(request, "network/newpost.html")

def all_post(request):
    # Grab all posts from database to pass to template
    postList = Post.objects.all()

    #Grab page number for pagination purposes
    page = request.GET.get('p', 1)
    
    #Order posts by time and serialize time object
    postList = postList.order_by("-time").all()
    postList = [post.serialize for post in postList]

    #Paginate list and set page number
    paginateList = Paginator(postList,10)
    postList = paginateList.page(page)

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

@csrf_exempt
def profile(request, username):
    #Test to see if supplied username is valid argument and exists
    try:
        userObj = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    #Check for logged in user to know when to display follow button
    if request.user.is_authenticated:
        loggedIn = True
    else:
        loggedIn = False

    currentUser = request.user.get_username()

    #Check if user is alreaady following profile page owner
    if userObj.followers.filter(username=currentUser).exists():
        buttonVal = "Unfollow"
    else:
        buttonVal = "Follow"

    #Check if current user is the owner profile to hide follow button
    if username == currentUser:
        showButton = False
    else:
        showButton = True

    #Grab follower and following counts from database
    followers = userObj.followers.all().count()
    following = userObj.following.all().count()

    #Grab all postings from current owner of the profile page to display
    postList = Post.objects.filter(poster=username) 

    #Order posts by time and serialize time object
    postList = postList.order_by("-time").all()
    postList = [post.serialize for post in postList]

    #Grab page number for pagination purposes
    page = request.GET.get('p', 1)

    #Paginate list and set page number
    paginateList = Paginator(postList,10)
    postList = paginateList.page(page)

    return render(request, "network/profile.html", {
        "userObj": userObj,
        "followers": followers,
        "following": following,
        "loggedIn": loggedIn,
        "currentUser": currentUser,
        "buttonVal": buttonVal,
        "showButton": showButton,
        "postList": postList
    })
    
@csrf_exempt
@login_required
def follow(request, owner):
    #Check to see if requested profile owner exists
    try:
        userObj = User.objects.get(username=owner)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    #Grab currently logged in user object from database
    follower = User.objects.get(username=request.user)
    
    #Toggle follower status inside user profile database
    if request.method == "PUT":
        #Grab json data to verify if user is following or unfollowing
        data = json.loads(request.body)
        if data.get("button") == "Follow":
            #Add a follower to the owner of the profile page/add following on the follower database
            userObj.followers.add(follower)
            follower.following.add(userObj)
        else: 
            #Remove a follower from the owner of profile page/remove following on follower database
            userObj.followers.remove(follower)
            follower.following.remove(userObj)
        #Update database and redirect to profile page
        userObj.save()
        #For some reason this redirect is doing a put and I can't figure out why
        return HttpResponseRedirect(reverse("profile", args=[owner,]))

@login_required
def following(request):
    #Grab current user logged in and get corresponding model object from database
    currentUser = request.user.get_username() 
    userObj = User.objects.get(username=currentUser)

    #Empty lists to store incoming data
    postList = []
    flatList = []
    
    #Grab list of all users current user is following and generate posts based on that
    followingList = userObj.following.all()
    for following in followingList:
        postList.append(Post.objects.filter(poster=following.username))
        print(following.username)
    
    #Data inside list are still wrapped up in query sets so going to recursively loop to flatten list and get only post objects into list
    for set in postList:
        for obj in set:
            flatList.append(obj)

     #Order posts by time and serialize time object
    sortedList = sorted(flatList, key=lambda x: x.time)
    flatList = [post.serialize for post in flatList]
  
    print(sortedList)

    #Grab page number for pagination purposes
    page = request.GET.get('p', 1)

    #Paginate list and set page number
    paginateList = Paginator(flatList,10)
    flatList = paginateList.page(page)

    return render(request, "network/following.html", {
        "postList": flatList
    })