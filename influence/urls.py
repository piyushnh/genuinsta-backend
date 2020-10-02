"""influence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
# from django.conf import settings
# import os 

# if settings.DEBUG:

#     if os.environ.get('RUN_MAIN') or os.environ.get('WERKZEUG_RUN_MAIN'):
#         import ptvsd

#         print('hiiiiiiiiiiiiiiiiiiiiiiiiiii')

#         ptvsd.enable_attach(address=('localhost', 7913))
#         print('Debugger Attached!')

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^accounts/', include('apps.custom_account.urls')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    # url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^friendship/', include('apps.friendship.urls')),
    url(r'^auth/', include('apps.socialAuth.urls')),
    url(r'^user/', include('apps.users.urls')),
    url(r'^post/', include('apps.posts.urls')),
    url(r'^notification/', include('apps.notification.urls')),
    url(r'^$', views.HomeView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
