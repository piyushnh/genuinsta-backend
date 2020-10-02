from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from .tokenAuthMiddleware import TokenAuthMiddlewareStack
# # import apps.restaurant_merchants.routing
# from apps.users.routing import websocket_urlpatterns
from apps.notification.routing import notif_urlpatterns
application = ProtocolTypeRouter({
    # # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(TokenAuthMiddlewareStack(
        URLRouter(
            notif_urlpatterns
        )
    )),

    # 'http': URLRouter(notif_urlpatterns),

})
