from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/shapes/$', consumers.ShapesConsumer.as_asgi()),
]
"""
This module defines the routing configuration for WebSocket connections in the application.

The `websocket_urlpatterns` list contains the URL patterns for WebSocket connections.
In this case, there is a single URL pattern defined: 'ws/shapes/'.

The `ShapesConsumer` class from the `consumers` module is used as the consumer for the WebSocket connection.

Note: This module requires Django to be installed.
"""
