# Generated by Django 3.0.8 on 2020-07-26 19:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_auto_20200726_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='_user_following_+', to=settings.AUTH_USER_MODEL),
        ),
    ]