from django.contrib import admin
from .models import (
        Post,
        Comment,
        Tag,
        HashTag,
        Like,
        Bookmark
)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(HashTag)
admin.site.register(Like)
admin.site.register(Bookmark)


# Register your models here.
