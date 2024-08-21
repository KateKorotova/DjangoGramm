from django.contrib import admin

from .models import Post, Image, Tag


admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Tag)
