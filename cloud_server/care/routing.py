from django.urls import re_path
from . import websockets

websocket_urlpatterns = [
    re_path(r"ws/vitals/$", websockets.VitalSignsConsumer.as_asgi()), # Example
]