"""Recipe URLs"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from recipe.views import RecipeViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r"recipes", RecipeViewSet)
# The basename is used to create the URL names for the viewset
app_name = "recipe"

urlpatterns = [
    path("", include(router.urls)),  # Include the router URLs
]
