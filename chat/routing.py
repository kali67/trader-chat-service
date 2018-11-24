from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from .middleware import TokenAuthMiddleware


from . import consumers


application = ProtocolTypeRouter(
    {
        "websocket": TokenAuthMiddleware(
        URLRouter([
            url(r'^ws/chat/(?P<conversation_id>[^/]+)/.*$', consumers.ChatConsumer),
        ])
        ),
    }
)