from django.test import TestCase
from apps.urlshortener.models import ShortenedURL


class URLShortenerTests(TestCase):
    def test_shorten_url_rate_limit(self):
        response = self.client.post('/api/v1/shorten/', {'long_url': 'https://example.com'})
        self.assertEqual(response.status_code, 429)
        self.assertIn('error', response.json())

    def test_shorten_url(self):
        response = self.client.post('/api/v1/shorten/', {'long_url': 'https://example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('short_url', response.json()["data"])

    def test_redirect_url(self):
        obj = ShortenedURL.objects.create(long_url='https://example.com', short_code='abc123')
        response = self.client.get(f'/api/v1/{obj.short_code}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, obj.long_url)
