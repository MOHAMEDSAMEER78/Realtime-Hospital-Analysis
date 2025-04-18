"""
ASGI config for cloud_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import care.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cloud_server.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(care.routing.websocket_urlpatterns),
})

