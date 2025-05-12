"""
Tests for the User API.
This module contains unit tests for the User API endpoints.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**kwargs):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Test the public features of the User API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@test.com",
            "password": "testpass",
            "name": "Test User",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)
        self.assertEqual(res.data["email"], payload["email"])

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            "email": "test@test.com",
            "password": "testpass",
            "name": "Test User",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            res.data["email"],
            ["user with this email already exists."],
        )

    def test_password_too_short_error(self):
        """Test error returned if password is too short."""
        payload = {
            "email": "test@gmail.com",
            "password": "pw",
            "name": "Test User",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
        self.assertEqual(
            res.data["password"],
            ["Ensure this field has at least 5 characters."],
        )

    def test_create_token_for_user(self):
        """Test that a token is created for the user."""
        user_details = {
            "email": "test@test.com",
            "password": "testpass",
            "name": "Test User",
        }
        create_user(**user_details)
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""
        create_user(email="test@test.com", password="testpass")
        payload = {"email": "test@test.com", "password": "wrongpassword"}

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_black_credentials(self):
        """Test that token is not created if no credentials are given."""
        res = self.client.post(TOKEN_URL, {})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test that token is not created if no password is given."""
        payload = {"email": "test@test.com", "password": ""}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test that authentication is required for users."""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email="test@test.com", password="pass1234", name="Test user"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_user_success(self):
        """Test the user authenticate and retrived successfull"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data,
            {
                "name": self.user.name,
                "email": self.user.email,
            },
        )

    def test_post_me_not_allowed(self):
        """Test that user cannot be retrieved with invalid credentials."""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test that user update successfully"""
        payload = {
            "name": "Test besu",
            "password": "newpassword123",
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
