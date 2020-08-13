from django.urls import path
from .consumers import NotificationConsumer


notif_urlpatterns = [
    path('ws/getNotifications/', NotificationConsumer),
]