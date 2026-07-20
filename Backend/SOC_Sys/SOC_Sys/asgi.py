"""
ASGI config for SOC_Sys project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import SOC_App.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SOC_Sys.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            SOC_App.routing.websocket_urlpatterns
        )
    ),
})
