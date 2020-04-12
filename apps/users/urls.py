from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from .views import (UserDetails,)

urlpatterns = [
    
    url(r'^details/(?P<pk>[\w-]+)/$',
            view = UserDetails.as_view(),
             name="user_details" ),
             


]
