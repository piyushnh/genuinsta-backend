from django.contrib import admin
from .models import (
        Post,
        Comment,
        Tag,
        Like,
        Bookmark
)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Bookmark)


# Register your models here.
