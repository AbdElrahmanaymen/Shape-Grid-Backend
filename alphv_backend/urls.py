
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("shapes/", include("base.urls")),
]

"""
URL Configuration for the AlphaV Backend.

This module defines the URL patterns for the AlphaV Backend application.
The urlpatterns list contains the paths for the admin site and the shapes app.
"""
