from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from .views import (notify,  set_fcm_token, get_notifications, mark_as_read, sendify)

urlpatterns = [
    
    
    path('notify/',
            view = notify,
             name="notify" ),
    path('setFCMToken/',
            view = set_fcm_token,
             name="set_fcm_token" ),
    path('getNotifications/',
            view = get_notifications,
             name="get_notifications" ),
  
    path('markAsRead/',
            view = mark_as_read,
             name="mark_as_read" ),
    path('sendify/',
            view = sendify,
             name="sendify" ),
  

    
             


]