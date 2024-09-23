"""
ASGI config for dcan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Ensure settings are loaded before anything else
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dcan.settings')

# Initialize Django ASGI application to ensure AppRegistry is loaded before importing other components
django_asgi_app = get_asgi_application()

# Now import your routing after the apps are loaded
import chatroom.routing
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.


django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                chatroom.routing.websocket_urlpatterns
            )
        )
    ),
})
