"""
Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        email = "test@test.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_user_with_email_normalizes_email(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ["test1@EXAMPLE.COM", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password="test123")
            self.assertEqual(user.email, expected)

    def test_create_user_without_email_raises_error(self):
        """Test creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="test123")

    def test_create_superuser_with_email_successful(self):
        """Test creating a superuser with an email is successful"""
        email = "test@gmail.com"
        password = "testpass123"

        user = get_user_model().objects.create_superuser(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
