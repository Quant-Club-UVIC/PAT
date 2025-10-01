from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


def get_request_data(email, password) -> dict:
    data = {}
    if email is not None:
        data['email'] = email

    if password is not None:
        data['password'] = password

    return data


class RegisterTests(APITestCase):

    def setUp(self):
        self.url = reverse('register')

    def test_register_success(self):
        data = get_request_data("user@gmail.com", "password123")
        response: Response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("Success!", response.data['message'])
        # check that user is created in db
        self.assertTrue(User.objects.filter(email=data['email']).exists())
        user = User.objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertTrue(user.is_active)

    def test_register_email_with_spaces(self):
        data = get_request_data(" user@gmail.com ", "password123")
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="user@gmail.com").exists())

    def test_register_duplicate_email(self):
        data = get_request_data("user@gmail.com", "password123")
        User.objects.create_user(email=data['email'], password=data['password'])

        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Account already exists.")
        self.assertEqual(User.objects.filter(email=data["email"]).count(), 1)

    def test_register_missing_email(self):
        data = get_request_data(None, "password123")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email is required.")
        self.assertEqual(User.objects.count(), 0)

    def test_register_blank_email(self):
        data = get_request_data("", "password123")
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(User.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Email is required.")

    def test_register_invalid_email_format(self):
        data = get_request_data("not-an-email", "password123")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Enter a valid email address.")
        self.assertEqual(User.objects.count(), 0)

    def test_register_password_too_short(self):
        data = get_request_data("user@gmail.com", "123")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Password is too short.")
        self.assertEqual(User.objects.count(), 0)

    def test_register_missing_password(self):
        data = get_request_data("user@gmail.com", None)
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(User.objects.count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Password is required.")
        self.assertEqual(User.objects.count(), 0)

    def test_register_blank_password(self):
        data = get_request_data("user@gmail.com", "")
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Password is required.")
        self.assertEqual(User.objects.count(), 0)

    def test_register_server_error(self):
        data = get_request_data("user@gmail.com", "password123")
        # Use patch as a context manager
        with patch('users.serializers.register_serializer.RegisterSerializer.save') as mock_save:
            mock_save.side_effect = Exception("Simulated server error")

            response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data['error'],
            "An unexpected error occurred. Please try again later."
        )
        self.assertEqual(User.objects.count(), 0)
