from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from . import views

from .views import (exchange_token,
                    exchange_auth_code,
                    authenticate
                    )

urlpatterns = [
    url(r'^social/exchange_token/(?P<backend>[\w-]+)/$',
            view = exchange_token,
             name="exchange_token" ),
    url(r'^social/exchange_auth/$',
            view = exchange_auth_code,
             name="exchange_auth_code" ),
    url(r'^social/authenticate/$',
            view = authenticate,
             name="authenticate" ),
]