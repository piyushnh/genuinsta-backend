from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from .views import (get_post, get_user_bookmarks, like_unlike_post, get_user_posts )

urlpatterns = [
    
    
    path('getPost/<postId>/',
            view = get_post,
             name="get_post" ),
    path('getUserPosts/<userId>/',
            view = get_user_posts,
             name="get_user_posts" ),
    path('getBookmarks/<userId>/',
            view = get_user_bookmarks,
             name="get_bookmarks" ),
    
    path('likeUnlikePost/<postId>/',
            view = like_unlike_post,
             name="like_unlike_post" ),
    
             


]