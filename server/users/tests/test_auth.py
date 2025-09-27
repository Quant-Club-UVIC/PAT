import http.cookies

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.conf import settings

User = get_user_model()
USER_DATA = {
    'email': 'test@gmail.com',
    'password': 'longpassword123'
}

class AuthTests(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(
            email=USER_DATA['email'],
            password=USER_DATA['password']
        )

    def test_login_returns_access_and_refresh_token(self):
        url = reverse('login')
        data = USER_DATA.copy()

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Should return 200 status")

        data: dict = response.data;
        self.assertIsNotNone(data, "Data should not be None")
        self.assertIsNotNone(data["access_token"], "Token should not be None")
        self.assertTrue(len(data["access_token"]) != 0, "Token should have access")

        refresh_cookie = response.cookies.get("refresh_token")
        self.assertIsNotNone(refresh_cookie, "Refresh token cookie should be set")
        self.assertTrue(len(refresh_cookie.value) > 0, "Refresh token should not be empty")

        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["httponly"], refresh_cookie["httponly"])
        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["secure"], refresh_cookie["secure"])
        self.assertEqual(settings.REFRESH_TOKEN_COOKIE["samesite"], refresh_cookie["samesite"])


