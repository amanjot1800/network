
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
    path("p/<str:username>", views.profile, name="profile"),
]
