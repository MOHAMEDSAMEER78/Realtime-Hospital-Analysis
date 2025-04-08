from django.urls import path
from . import views

websocket_urlpatterns = [
    # Define your WebSocket URL patterns in care/routing.py
]

urlpatterns = [
    path('receive_fog_data/', views.receive_fog_data, name='receive_fog_data'),
]
