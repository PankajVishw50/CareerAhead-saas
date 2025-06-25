"""
ASGI config for careerahead project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# important: it configures application, shifting this line below could cause errors
os.environ.setdefault("django_settings_module", "careerahead.settings")
asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack, CookieMiddleware, SessionMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
import django

from chat.middlewares import WebSocketLoggerMiddleware
from chat.routing import websocket_urlpatterns
from account.auth import WebSocketTokenAuthenticationMiddleware


application = ProtocolTypeRouter(
    {
        "http": asgi_application,
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
