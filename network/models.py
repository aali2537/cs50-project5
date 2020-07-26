from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.CharField(max_length=64)
    content = models.TextField()
    time = models.DateTimeField()
    likes = models.IntegerField(default=0)