from django.contrib import admin
from django.urls import path, include, reverse
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path("docs/", include("core.swagger.api.urls")),
    path("health/", include("core.health.api.urls")),
    path("auth/", include("features.authentication.api.urls")),
    path("users/", include("features.users.api.urls")),
    path("rooms/", include("features.rooms.api.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("", lambda _: redirect(reverse("swagger-ui"))))
