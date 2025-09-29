import http.cookies
from unittest.mock import patch

from django.contrib.auth import get_user_model
from psycopg2 import OperationalError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.conf import settings

User = get_user_model()
USER_DATA = {
    'email': 'test@gmail.com',
    'password': 'longpassword123'
}

ACCESS_TOKEN_KEY = settings.ACCESS_TOKEN_KEY;
REFRESH_TOKEN_KEY = settings.REFRESH_TOKEN_COOKIE['key']


class LoginTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email=USER_DATA['email'],
            password=USER_DATA['password']
        )

    def test_login_returns_access_and_refresh_token_on_success(self):
        url = reverse('login')
        user_data = USER_DATA.copy()

        response = self.client.post(url, user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Should return 200 status")

        data: dict = response.data;
        self.assertIsNotNone(data, "Data should not be None")
        self.assertIsNotNone(data[ACCESS_TOKEN_KEY], "Token should not be None")
        self.assertTrue(len(data[ACCESS_TOKEN_KEY]) != 0, "Token should have access")
        self.assertNotIn(REFRESH_TOKEN_KEY, data, "Response body should not contain refresh token")

        refresh_cookie = response.cookies.get(REFRESH_TOKEN_KEY)
        self.assertIsNotNone(refresh_cookie, "Refresh token cookie should be set")
        self.assertTrue(len(refresh_cookie.value) > 0, "Refresh token should not be empty")

        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["httponly"], refresh_cookie["httponly"])
        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["secure"], refresh_cookie["secure"])
        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["samesite"], refresh_cookie["samesite"])
        self.assertEqual(int(refresh_cookie["max-age"]), settings.REFRESH_TOKEN_COOKIE["max_age"])

    def test_login_with_wrong_credentials(self):
        url = reverse('login')

        response: Response = self.client.post(url, {
            'email': 'wrongEmail@gmail.com',
            'password': 'wrongPassword123'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(ACCESS_TOKEN_KEY, response.data)
        self.assertIsNone(response.cookies.get(REFRESH_TOKEN_KEY))

        data = response.data
        self.assertIsNotNone(data)
        self.assertEqual("Invalid email and/or password", data.get('error'))

    def test_login_with_missing_fields(self):
        url = reverse('login')
        data = USER_DATA.copy()

        response = self.client.post(url, {
            'email': data.get('email'),
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(ACCESS_TOKEN_KEY, response.data)
        self.assertIsNone(response.cookies.get(REFRESH_TOKEN_KEY))

        data = response.data
        self.assertIsNotNone(data)
        self.assertEqual("Invalid email and/or password", data.get('error'))

    def test_login_fails_when_db_unavailable(self):
        url = reverse('login')
        user_data = USER_DATA.copy()

        with patch.object(User.objects, "get", side_effect=OperationalError("DB connection lost")):
            response = self.client.post(url, user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.data
        self.assertIsNotNone(data)
        self.assertEqual("Unexpected error occurred. Try again later", data.get('error'))