from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
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
    @method_decorator(ratelimit(key='ip', rate='1/m', method='POST', block=False))
    def post(self, request):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Try again in 1 minute'}, status=429)
        request_body = CreateShortenedURLRequestBody(data=get_request_data(request))
        request_body.is_valid(raise_exception=True)
        data = request_body.data
        long_url = data["long_url"]
        shortened_url, _ = ShortenedURL.objects.get_or_create(
            long_url=long_url,
            defaults={"short_code": ShortenedURL.generate_unique_short_code()}
        )
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

    @method_decorator(ratelimit(key='ip', rate='1/m', method='GET', block=False))
    def get(self, request, *args, **kwargs):
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            return JsonResponse({'error': 'Try again in 1 minute'}, status=429)
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
