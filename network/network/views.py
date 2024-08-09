import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from network.models import User, Post, Follow, Like
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.serializers import serialize
from django.core.paginator import Paginator

# I got lost and ran out of time for this assignment :'(
def index(request):
    posts = Post.objects.all().order_by("id").reverse()
    return render(request, "network/index.html", {
        "posts": posts
    })


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

@login_required
@csrf_exempt
def new_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get('content')
        user_id = request.user.id

        if content is not None:
            user = User.objects.get(pk=request.user.id)
            post = Post(user=user, post=content)
            post.save()
            return HttpResponseRedirect(status=201)
        else:
            return JsonResponse({"error": "Invalid post content"}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
    
def all_posts(request):
    posts = Post.objects.all().order_by("id").reverse()

    # Fetch usernames associated with each post
    post_data = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "user_id": post.user.id,
            "user": post.user.username if post.user else None,  # Get the username or None if user is not set
            "post": post.post,
            "time_date": post.time_date
        }
        post_data.append(post_dict)

    return JsonResponse(post_data, safe=False)

def profile(request, user_id):
    user_profile = User.objects.get(pk=user_id)  # Fetch user based on user_id from URL
    posts = Post.objects.filter(user=user_profile).order_by("time_date").reverse()  # Filter posts by user_profile
    followers_count = Follow.objects.filter(user=user_profile).count()
    following_count = Follow.objects.filter(follower=user_profile).count()
    #CS50.ai: The Q objects are used to create complex queries in Django. In this case, it's creating a logical AND condition. The filter method returns a QuerySet that matches the conditions, and exists() checks if there is at least one record in the QuerySet.
    is_following = Follow.objects.filter(Q(user=request.user.id) & Q(follower=user_profile)).exists()  # Check if current user is following user_profile

    return render(request, "network/profile.html", {
        "username": user_profile.username,  # Pass user_profile.username instead of request.user.username
        "user_profile": user_profile,
        "posts": posts,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
        "USER_ID": request.user.id
    })

def follow(request):
    # Create a follow relationship
    followuser = request.POST['followuser']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username = followuser)
    f = Follow(user = currentUser, follower=userfollowData)
    f.save()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    #opposite of follow with checking relationship before deleting
    if request.method == 'POST':
        followuser = request.POST.get('followuser')
        if followuser:
            currentUser = User.objects.get(pk=request.user.id)
            userfollowData = get_object_or_404(User, username=followuser)
            # Check if the follow relationship exists before attempting to delete
            follow_object = Follow.objects.filter(user=currentUser, follower=userfollowData).first()
            if follow_object:
                follow_object.delete()
                user_id = userfollowData.id
                return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))
      
def following(request):
    current_user = request.user
    following = Follow.objects.filter(user=current_user).values_list('follower__id', flat=True)
    
    # Retrieve posts made by users followed by the current user
    posts_following = Post.objects.filter(user_id__in=following).order_by('-time_date')

    # Pagination
    paginator = Paginator(posts_following, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "page_posts": page_posts
    })  


def edit(request):
    pass

def like(request):
    pass