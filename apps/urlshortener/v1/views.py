from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from apps.common.messages import SUCCESS_MESSAGE
from apps.common.utils import format_response, get_request_data
from apps.urlshortener.models import ShortenedURL
from apps.urlshortener.v1.serializers import CreateShortenedURLRequestBody, ShortenedUrlSerializer
from config.settings.base import BASE_SHORTENED_URL


# View for shortening URLs
class ShortenedUrlView(APIView):
    def post(self, request):
        request_body = CreateShortenedURLRequestBody(data=get_request_data(request))
        request_body.is_valid(raise_exception=True)
        data = request_body.data
        long_url = data["long_url"]
        shortened_url = ShortenedURL.objects.filter(long_url=long_url)
        if shortened_url:
            ret_data = {"short_url": f"{BASE_SHORTENED_URL}{shortened_url[0].short_code}"}
        else:
            shortened_url = ShortenedURL(long_url=data["long_url"])
            shortened_url.short_code = shortened_url.generate_unique_short_code()
            shortened_url.save()
            ret_data = {"short_url": f"{BASE_SHORTENED_URL}{shortened_url.short_code}"}

        # Format response
        response = format_response(
            data=ret_data,
            message=SUCCESS_MESSAGE,
            status_code=status.HTTP_200_OK,
        )
        return response


class ShortenedUrlListView(ListAPIView):
    serializer_class = ShortenedUrlSerializer

    def get_queryset(self):
        queryset = ShortenedURL.objects.filter()
        return queryset

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        data = response.data

        # Format response
        response = format_response(
            data=data,
            message=SUCCESS_MESSAGE,
            status_code=status.HTTP_200_OK,
        )
        return response


# View for redirecting short URLs
class RedirectURLView(APIView):
    def get(self, request, short_code):
        shortened_url_obj = get_object_or_404(ShortenedURL, short_code=short_code)
        return redirect(shortened_url_obj.long_url)
