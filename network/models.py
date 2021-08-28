from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.DO_NOTHING, related_name="posts")
    body = models.CharField(max_length=500, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes_users = models.ManyToManyField("User", related_name='liked_posts', blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes_count": self.likes_users.all().count(),
            "likes_users": [user.username for user in self.likes_users.all()]
        }

