"""
ASGI config for careerahead project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack, CookieMiddleware, SessionMiddleware
from channels.security.websocket import AllowedHostsOriginValidator

from chat.middlewares import WebSocketLoggerMiddleware
from chat.routing import websocket_urlpatterns
from account.auth import WebSocketTokenAuthenticationMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "careerahead.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WebSocketLoggerMiddleware(
            CookieMiddleware(
                SessionMiddleware(
                    WebSocketTokenAuthenticationMiddleware(
                        URLRouter(websocket_urlpatterns)
                    ),
                )
            ),
        ),
    }
)
