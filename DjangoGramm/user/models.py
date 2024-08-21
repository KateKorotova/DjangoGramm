from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.jpg', blank=True, null=True)

    def __str__(self):
        return self.username
