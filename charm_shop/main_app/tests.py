from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from .views import all_products


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_url_allowed_hosts(self):
        response = self.c.get('')
        self.assertEqual(response.status_code, 200)

    def test_all_products_html(self):
        request = HttpRequest()
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertEqual(response.status_code, 200)

    def test_view_function(self):
        request = self.factory.get('/product/nike-running-shoes/')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertEqual(response.status_code, 200)
