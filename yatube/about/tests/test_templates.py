from django.test import TestCase, Client


class StaticURLTemplatesTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_tech_tamplate(self):
        response = self.guest_client.get("/about/tech/")
        self.assertTemplateUsed(response, "about/tech.html")

    def test_author_tamplate(self):
        response = self.guest_client.get("/about/author/")
        self.assertTemplateUsed(response, "about/author.html")
