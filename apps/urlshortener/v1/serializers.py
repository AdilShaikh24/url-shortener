from rest_framework import serializers

from apps.urlshortener.models import ShortenedURL
from config.settings.base import BASE_SHORTENED_URL


class CreateShortenedURLRequestBody(serializers.Serializer):
    long_url = serializers.URLField(required=True)


class ShortenedUrlSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = "__all__"

    def get_short_url(self, obj):
        return f"{BASE_SHORTENED_URL}{obj.short_code}"
