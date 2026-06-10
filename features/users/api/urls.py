from django.urls import path, include
from rest_framework import routers

from features.users.api import viewsets
from features.users.api import views

users_router = routers.SimpleRouter()
users_router.register("", viewsets.UserViewSet, basename="users")

urlpatterns = [
    path("me/", views.MeAPIView.as_view(), name="me"),
    path("", include(users_router.urls)),
]
