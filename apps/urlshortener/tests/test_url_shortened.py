from django.test import TestCase
from rest_framework import status
from apps.urlshortener.models import ShortenedURL


class ShortenedUrlViewTests(TestCase):
    def setUp(self):
        self.valid_url = "http://example.com"
        self.shorten_url_endpoint = "/api/v1/shorten/"
        self.invalid_url = "invalid-url"
        self.blank_url = ""

    def test_shorten_url_success(self):
        """Ensure that a valid URL is shortened successfully."""
        response = self.client.post(self.shorten_url_endpoint, {"long_url": self.valid_url},
                                    REMOTE_ADDR='192.168.1.100')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("short_url", response.json()["data"])

    def test_shorten_url_rate_limit(self):
        """Ensure rate limiting works properly."""
        for _ in range(2):  # Exceed rate limit (1 request per minute)
            response = self.client.post(self.shorten_url_endpoint, {"long_url": self.valid_url})
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
        self.assertIn("error", response.json())

    def test_shorten_url_existing(self):
        """Ensure that shortening the same URL returns the same short code."""
        obj = ShortenedURL.objects.create(long_url=self.valid_url, short_code="abc123")
        response = self.client.post(self.shorten_url_endpoint, {"long_url": self.valid_url}, REMOTE_ADDR='192.168.1.101')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["short_url"], f"http://short.ner/{obj.short_code}")

    def test_shorten_invalid_url(self):
        """Ensure that an invalid URL returns a 400 Bad Request."""
        response = self.client.post(self.shorten_url_endpoint, {"long_url": self.invalid_url}, REMOTE_ADDR='192.168.1.102')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("long_url", response.json())

    def test_shorten_blank_url(self):
        """Ensure that a blank URL returns a 400 Bad Request."""
        response = self.client.post(self.shorten_url_endpoint, {"long_url": self.blank_url})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("long_url", response.json())


class ShortenedUrlListViewTests(TestCase):
    def setUp(self):
        self.list_url_endpoint = "/api/v1/shortened-urls/"
        self.url1 = ShortenedURL.objects.create(long_url="http://example1.com", short_code="xyz123")
        self.url2 = ShortenedURL.objects.create(long_url="http://example2.com", short_code="abc789")

    def test_list_shortened_urls_success(self):
        """Ensure all shortened URLs are listed correctly."""
        response = self.client.get(self.list_url_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()["data"]), 2)

    def test_list_urls_rate_limit(self):
        """Ensure rate limiting works on the list endpoint."""
        for _ in range(2):  # Exceed rate limit
            response = self.client.get(self.list_url_endpoint)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class RedirectURLViewTests(TestCase):
    def setUp(self):
        self.url_obj = ShortenedURL.objects.create(long_url="http://example.com", short_code="abc123")

    def test_redirect_url_success(self):
        """Ensure redirection works when a valid short code is provided."""
        response = self.client.get(f'/api/v1/{self.url_obj.short_code}/')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, self.url_obj.long_url)

    def test_redirect_url_not_found(self):
        """Ensure a 404 is returned for an invalid short code."""
        response = self.client.get("/api/v1/invalid-code/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
