from django.test import TestCase, Client
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from django.http import HttpRequest

from account.models import User
from account.auth import login, Token, encrypt
from util.tests.baseTest import BaseTestCase, UserAuthedTestCase, BaseAuthedTestCase


class LoginTest(BaseTestCase):
    fixtures = ["sampleData.json"]

    def test_success_login_cookie(self):
        """Try to login to sahil
        with refresh_token returned in cookie (default behaviour)
        """
        response = self.client.post(
            reverse("api:login"), content_type="application/json", data=self.user1_data
        )
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.accepted_media_type)

        self.assertFalse(data.get("refresh_token"))
        self.assertTrue(data.get("access_token"))
        self.assertTrue(response.cookies.get(settings.TOKEN_REFRESH_KEY))

    def test_success_login_body(self):
        """Test Login with
        refresh_token returned in body
        """

        try:
            response = self.client.post(
                reverse("api:login"),
                content_type="application/json",
                data={**self.user1_data, "in_body": True, "in_cookie": False},
            )
            data = response.json()
        except ValueError:
            pass

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.accepted_media_type)

        self.assertTrue(data.get("access_token"))
        self.assertTrue(data.get("refresh_token"))
        self.assertFalse(response.cookies.get(settings.TOKEN_REFRESH_KEY))

    def test_success_login_body_2(self):
        """Test Login with
        refresh_token returned in body and also in cookie
        """

        response = self.client.post(
            reverse("api:login"),
            content_type="application/json",
            data={**self.user1_data, "in_body": True, "in_cookie": True},
        )
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.accepted_media_type)

        self.assertTrue(data.get("access_token"))
        self.assertTrue(data.get("refresh_token"))
        self.assertTrue(response.cookies.get(settings.TOKEN_REFRESH_KEY))

    def test_success_login_no_refresh_token(self):
        """Test Login to jatin with
        refresh_token not returned
        """
        response = self.client.post(
            reverse("api:login"),
            content_type="application/json",
            data={**self.user1_data, "in_body": False, "in_cookie": False},
        )
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.accepted_media_type)

        self.assertTrue(data.get("access_token"))
        self.assertFalse(data.get("refresh_token"))
        self.assertFalse(response.cookies.get(settings.TOKEN_REFRESH_KEY))

    def test_success_login_access_protected_endpoint(self):
        """Test to access protected page
        after successfull login
        """

        response = self.client.post(
            reverse("api:login"),
            content_type="application/json",
            data={**self.user1_data, "in_body": True, "in_cookie": False},
        )
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertEqual("application/json", response.accepted_media_type)

        self.assertTrue(data.get("access_token"))
        self.assertTrue(data.get("refresh_token"))
        self.assertFalse(response.cookies.get(settings.TOKEN_REFRESH_KEY))

        # Access Protected view
        response = self.client.get(
            reverse("api:signed-token"),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {data.get('access_token')}",
        )
        data = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(data.get("token"))


class AccessTokenTest(UserAuthedTestCase):

    def test_get_access_token_pass_refresh_in_body(self):
        """Fetch access token"""

        response = self.client.post(
            reverse("api:access-token"), data={"refresh_token": self.refresh_token}
        )
        json = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(json.get("access_token"))

    def test_get_access_token_pass_refresh_in_cookie(self):
        """Fetch access token by passing
        refresh token in cookie
        """

        response = self.authed_client.post(
            reverse("api:access-token"),
        )
        json = response.json()

        self.assertEqual(200, response.status_code)
        self.assertTrue(json.get("access_token"))

    def test_get_access_without_refresh(self):

        response = self.client.post(
            reverse("api:access-token"),
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_access_with_invalid_refresh(self):

        response = self.client.post(
            reverse("api:access-token"),
            data={"refresh_token": "kfljekfjlekfjelwifjoelwkfjlefjkwoe"},
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class LogoutTest(UserAuthedTestCase):

    def test_logout_refresh_in_cookie(self):

        response = self.authed_client.post(reverse("api:logout"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_logout_refresh_in_cookie_without_auth(self):

        response = self.authed_client.post(
            reverse("api:logout"),
            HTTP_AUTHORIZATION=None,
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_logout_refresh_in_body_without_auth(self):

        response = self.client.post(
            reverse("api:logout"),
            data={
                "refresh_token": self.refresh_token,
            },
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_access_before_and_after_logout_refresh_in_cookie(self):

        # Fetch access before logout
        response = self.authed_client.post(reverse("api:access-token"))
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(json.get("access_token"))

        # Logout
        response = self.authed_client.post(reverse("api:logout"))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Fetch access after logout
        response = self.authed_client.post(reverse("api:access-token"))

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_access_before_and_after_logout_refresh_in_body(self):

        # Fetch access before logout
        response = self.client.post(
            reverse("api:access-token"), data={"refresh_token": self.refresh_token}
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(json.get("access_token"))

        # Logout
        response = self.client.post(
            reverse("api:logout"),
            data={
                "refresh_token": self.refresh_token,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Fetch access after logout
        response = self.client.post(
            reverse("api:access-token"),
            data={
                "refresh_token": self.refresh_token,
            },
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_get_access_before_and_after_failed_logout_refresh_in_body(self):

        # Fetch access before logout
        response = self.client.post(
            reverse("api:access-token"), data={"refresh_token": self.refresh_token}
        )
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(json.get("access_token"))

        # Logout
        response = self.client.post(
            reverse("api:logout"),
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # Fetch access after logout
        response = self.client.post(
            reverse("api:access-token"),
            data={
                "refresh_token": self.refresh_token,
            },
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)


class SignedTokenTest(UserAuthedTestCase):

    def test_get_signed_token(self):

        response = self.authed_client.get(reverse("api:signed-token"))
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(json.get("token"))

    def test_get_signed_token_without_auth(self):

        response = self.client.get(reverse("api:signed-token"))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_protected_view(self):
        response = self.authed_client.get(reverse("api:signed-token"))
        json = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue(json.get("token"))

        signed_token = json.get("token")

        # access protected view without signed token
        response = self.client.post(
            reverse("api:verify_recharge", kwargs={"recharge_id": "a"})
        )

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

        # access protected view with signed token
        response = self.client.post(
            reverse("api:verify_recharge", kwargs={"recharge_id": "a"}),
            query_params={"token": signed_token},
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
