from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.CharField(max_length=64)
    content = models.TextField()
    time = models.DateTimeField()
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "poster": self.poster,
            "content": self.content,
            "time": self.time.strftime("%I:%M %p - %b %d, %Y"),
            "likes": self.likes
        }