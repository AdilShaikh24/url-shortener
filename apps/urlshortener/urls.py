"""
urls.py
Contain urls for the urlshortner.
"""
# Third Party Imports
from django.urls import include, path

from apps.urlshortener.v1.views import ShortenedUrlListView

app_name = "urlshortener"
urlpatterns = [
    path("v1/shortened-urls/", ShortenedUrlListView.as_view(), name="v1-shortened-urls"),
    path("v1/", include("apps.urlshortener.v1.urls")),
]