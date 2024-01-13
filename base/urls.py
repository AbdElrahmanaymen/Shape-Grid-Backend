from django.urls import path
from . import views

urlpatterns = [
    path('', views.shapes_view, name='shapes_view'),
]
"""
URL patterns for the base app.

This module defines the URL patterns for the base app. It includes a single URL pattern
that maps the root URL to the shapes_view function in the views module.

Example:
    urlpatterns = [
        path('', views.shapes_view, name='shapes_view'),
    ]
"""
