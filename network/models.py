from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', blank=True)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    poster = models.CharField(max_length=64)
    content = models.TextField()
    time = models.DateTimeField()
    likes = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, blank=True)

    def serialize(self):
        return {
            "poster": self.poster,
            "content": self.content,
            "time": self.time.strftime("%I:%M %p - %b %d, %Y"),
            "likes": self.likes,
            "id": self.id,
            "liked": self.liked
        }