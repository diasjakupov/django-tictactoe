"""
ASGI config for tictactoe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""
import chat.routing
import game.routing
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from .middleware.tokemAuthMiddleWare import TokenAuthMiddleWare

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tictactoe.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":TokenAuthMiddleWare(
        URLRouter([
            *chat.routing.websocket_urlpatterns,
            *game.routing.websocket_urlpatterns
        ])
    )
})
