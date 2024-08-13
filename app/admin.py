from django.contrib import admin

from app.models import Post, Tag


@admin.register(Post)
class Post(admin.ModelAdmin):
    pass


@admin.register(Tag)
class Tag(admin.ModelAdmin):
    pass
