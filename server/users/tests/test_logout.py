from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from src.settings import REFRESH_TOKEN_COOKIE


class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("logout")

    def test_refresh_token_cookie_deleted(self):
        self.client.cookies[REFRESH_TOKEN_COOKIE["key"]] = "dummy_token"

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Logged out")

        deleted_cookie = response.cookies.get(REFRESH_TOKEN_COOKIE["key"])

        self.assertIsNotNone(deleted_cookie)
        self.assertEqual(deleted_cookie.value, "")
        self.assertEqual(deleted_cookie['max-age'], 0)
        self.assertEqual(deleted_cookie['path'], '/')

    def test_logout_without_cookie_still_successful(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Logged out")

