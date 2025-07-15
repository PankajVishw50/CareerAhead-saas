from rest_framework.urls import path

from user.views import (
    MeView,
    PublicUserView,
)

urlpatterns = [
    path("me", MeView.as_view(), name="me"),
    path("<uuid:pk>", PublicUserView.as_view(), name="user"),
]
