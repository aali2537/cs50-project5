# Generated by Django 3.0.8 on 2020-07-26 11:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_likedby'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likedBy',
        ),
        migrations.AddField(
            model_name='post',
            name='likedBy',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]