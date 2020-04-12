from django.urls import path


from . import consumers

websocket_urlpatterns = [
    path('ws/orderList/<str:restaurant_id>/', consumers.OrderListConsumer),
    path('ws/order/<str:order_id>/', consumers.OrderConsumer),
]