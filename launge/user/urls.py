"""
URLs for the user app.
"""

from django.urls import path
from user.views import UserCreateView, UserTokenView, ManageUserView

app_name = "user"
urlpatterns = [
    path("create/", UserCreateView.as_view(), name="create"),
    path("token/", UserTokenView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="me"),
]
