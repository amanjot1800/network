
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.fetch_posts, name="posts"),
    path("newpost", views.create_posts, name="new_post"),
    path("posts/<int:post_id>", views.update_posts, name="update_posts"),
    path("followingposts", views.following_posts_page, name="following_posts_page"),
    path("followingusersposts", views.following_posts, name="following_posts"),
    path("userposts/<str:user>", views.fetch_user_posts, name="user_posts"),
    path("p/<str:username>", views.profile, name="profile"),
]
