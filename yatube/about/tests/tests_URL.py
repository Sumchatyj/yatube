from django.test import TestCase, Client
from http import HTTPStatus


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author(self):
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, HTTPStatus.OK)
