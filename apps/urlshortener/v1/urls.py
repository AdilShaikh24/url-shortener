from django.urls import path

from apps.urlshortener.v1.views import ShortenedUrlView, RedirectURLView

urlpatterns = [
    path("shorten/", ShortenedUrlView.as_view(), name="v1-shorten-url"),
    path('<str:short_code>/', RedirectURLView.as_view(), name='redirect-url'),
]