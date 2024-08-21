from django.db import models

from user.models import CustomUser


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    alt_text = models.CharField(max_length=200, default='image')


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now_add=True)
    images = models.ManyToManyField(Image, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
