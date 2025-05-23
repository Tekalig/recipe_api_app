"""
Tests for Admin modifications
These tests are designed to ensure that the admin modifications are working as expected.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client


class AdminSiteTests(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a client and a superuser.
        """
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="test@test.com",
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="best@test.com",
            password="testpass123",
            name="Test User",
        )

    def test_users_listed(self):
        """
        Test that users are listed on the user page.
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """
        Test that the user edit page works.
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_create_user_page(self):
        """
        Test that the create user page works.
        """
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Add user")
