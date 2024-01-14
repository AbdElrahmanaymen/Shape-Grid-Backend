"""
ASGI config for alphv_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
import django
from django.core.asgi import get_asgi_application
from base.routing import websocket_urlpatterns
from channels.routing import get_default_application

import base.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alphv_backend.settings")

django.setup()

application = get_default_application()
