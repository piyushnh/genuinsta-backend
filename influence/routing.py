from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
# # import apps.restaurant_merchants.routing
from apps.users.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
    # # (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )),
})