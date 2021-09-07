import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html", {
        "title": "All posts",
    })


@csrf_exempt
def profile(request, username):

    if request.method == 'PUT':

        u = User.objects.get(username=request.user.username)
        pr_user = User.objects.get(username=username)

        if u in pr_user.followers.all():
            u.following.remove(pr_user)
        else:
            u.following.add(pr_user)
        u.save()
        return HttpResponse(status=204)

    following = False
    if request.user in User.objects.get(username=username).followers.all():
        following = True

    return render(request, "network/profile.html", {
        "puser": User.objects.get(username=username),
        "following": "Unfollow" if following else "Follow",
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


@csrf_exempt
def fetch_posts(request):
    all_posts = Post.objects.all()
    all_posts = all_posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in all_posts], safe=False)


@csrf_exempt
def fetch_user_posts(request, user):
    posts = Post.objects.filter(user=User.objects.get(username=user))
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


@login_required
@csrf_exempt
def create_posts(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post_text = data.get('text')

    new_post = Post(user=request.user, body=post_text)
    new_post.save()

    return JsonResponse({"message": "Post created successfully"}, status=201)


@csrf_exempt
def update_posts(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "post not found"}, status=404)

    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get('likes') is not None and data.get('likes'):
            post.likes_users.add(request.user)
        elif data.get('unlikes') is not None and data.get('unlikes'):
            post.likes_users.remove(request.user)
        post.save()
        return HttpResponse(status=204)


@login_required
@csrf_exempt
def following_posts(request):

    u = User.objects.get(username=request.user.username)
    following_users = u.following.all()
    posts = []

    for user in following_users:
        for post in user.posts.all():
            posts.append(post)

    return JsonResponse([post.serialize() for post in posts], safe=False)


def following_posts_page(request):
    return render(request, "network/followingposts.html")





