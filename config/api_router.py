"""
api_router.py
Contain routes for the project API.
"""

# Third Party Imports
from django.urls import include, path

urlpatterns = [
    path("", include("apps.urlshortener.urls", namespace="urlshortener")),
]