from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from .views import (get_user_profile, get_owner_profile)

urlpatterns = [
    
#     url(r'^details/(?P<pk>[\w-]+)/$',
#             view = UserDetails.as_view(),
#              name="user_details" ),
    path('profile/<userName>/',
            view = get_user_profile,
             name="get_user_profile" ),
    path('ownerProfile/',
            view = get_owner_profile,
             name="get_owner_profile" ),
             


]
