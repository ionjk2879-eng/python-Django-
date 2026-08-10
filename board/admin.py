from django.contrib import admin

from .models import Comment, Post, PostImage

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostImage)
