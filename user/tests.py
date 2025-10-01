import time
from datetime import timedelta
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class ViewProfileAPITest(APITestCase):
    @override_settings(
        SIMPLE_JWT={
            "ACCESS_TOKEN_LIFETIME": timedelta(seconds=1),
            "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
        }
    )

    def setUp(self):
        # common setup
        self.user = User.objects.create_user(username='normal-user', email='normal@usergmail.com', password='7')
        self.verify_url = reverse('profile', kwargs={'user_id': self.user.pk})

        # create tokens
        token_response = self.client.post(reverse('token_obtain_pair'),{"username": "normal-user", "password": "7"},format="json")
        self.access_token = token_response.data["access"]
        self.refresh_token = token_response.data["refresh"]

    def test_token_verify_success(self):
        response = self.client.get(self.verify_url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_access_token_refresh(self):
        time.sleep(2)

        # the last token is expired
        refresh_response = self.client.post(reverse('token_refresh'),{"refresh": self.refresh_token},format="json")
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

        # update the header with a new token
        new_access = refresh_response.data['access']
        response = self.client.get(self.verify_url,HTTP_AUTHORIZATION=f'Bearer {new_access}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutAPITest(APITestCase):
    def setUp(self):
        # common setup
        self.user = User.objects.create_user(username="user", email="user@gmail.com", password="7")
        self.logout_url = reverse('logout')

        # obtain tokens
        token_response = self.client.post(
            reverse('token_obtain_pair'),
            {"username": "user", "password": "7"},
            format="json"
        )
        self.access_token = token_response.data['access']
        self.refresh_token = token_response.data['refresh']

    def test_logout_success(self):
        response = self.client.post(
            self.logout_url,
            {"refresh": self.refresh_token},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['result'])

        # try using refresh-token after logout → should fail
        refresh_response = self.client.post(
            reverse('token_refresh'),
            {"refresh": self.refresh_token},
            format="json"
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
