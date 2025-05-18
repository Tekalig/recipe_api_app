"""
# Test the recipe API
# This test file is used to test the recipe API
"""

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

Recipe_URL = reverse("recipe:recipe-list")


def detail_url(recipe_id):
    """Create and return a recipe detail URL"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


def create_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        "title": "Sample Recipe",
        "time_minutes": 10,
        "price": 5.00,
        "link": "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITests(APITestCase):
    """Test the recipe API"""

    def test_create_recipe(self):
        """Test creating a recipe"""

        def setup(self):
            self.client = APIClient()

        def test_auth_required(self):
            """Test that authentication is required for creating a recipe"""
            response = self.client.post(Recipe_URL)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(APITestCase):
    """Test the recipe API"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="test123")
        self.client.force_authenticate(user=self.user)

    def test_retrive_recipe(self):
        """Test creating a recipe"""
        create_recipe(self.user)
        create_recipe(self.user)
        response = self.client.get(Recipe_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_limited_user_recipe(self):
        """Test retrieving recipes for authenticated user"""
        other_user = create_user(email="test@test.com", password="test123")
        create_recipe(other_user)
        create_recipe(self.user)
        response = self.client.get(Recipe_URL)
        recipes = Recipe.objects.filter(user=self.user).order_by("-id")
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_recipe(self):
        """Test retrieving a recipe detail"""
        recipe = create_recipe(self.user)
        url = detail_url(recipe.id)
        response = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(response.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            "title": "Sample Recipe",
            "time_minutes": 10,
            "price": 5.00,
            "link": "http://example.com/recipe.pdf",
        }
        response = self.client.post(Recipe_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data["id"])
        for key, value in payload.items():
            self.assertEqual(value, getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_partial_update_recipe(self):
        """Test updating a recipe with PATCH"""
        original_link = "http://example.com/recipe.pdf"
        recipe = create_recipe(
            user=self.user,
            title="Sample Recipe",
            link=original_link,
        )
        payload = {"title": "Updated Recipe"}
        url = detail_url(recipe.id)
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload["title"])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update_recipe(self):
        """Test updating a recipe with PUT"""
        recipe = create_recipe(
            user=self.user,
            title="Sample Recipe",
            link="http://example.com/recipe.pdf",
        )
        payload = {
            "title": "Updated Recipe",
            "time_minutes": 20,
            "price": 10.00,
            "link": "http://example.com/updated_recipe.pdf",
        }
        url = detail_url(recipe.id)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for key, value in payload.items():
            self.assertEqual(value, getattr(recipe, key))
        self.assertEqual(recipe.user, self.user)

    def test_update_user_error(self):
        """Test changing the recipe user results in an error"""
        new_user = create_user(email="test1@test.com", password="test123")

        recipe = create_recipe(user=self.user)

        payload = {"user": new_user.id}
        url = detail_url(recipe.id)

        response = self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = create_recipe(user=self.user)
        url = detail_url(recipe.id)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        recipes = Recipe.objects.filter(id=recipe.id)
        self.assertFalse(recipes.exists())

    def test_delete_other_user_recipe_error(self):
        """Test deleting a recipe that belongs to another user results in an error"""
        other_user = create_user(email="user@test.com", password="test123")

        recipe = create_recipe(user=other_user)
        url = detail_url(recipe.id)
        # Attempt to delete the recipe with the authenticated user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Check that the recipe still exists
        recipes = Recipe.objects.filter(id=recipe.id)
        self.assertTrue(recipes.exists())
