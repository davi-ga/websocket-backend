from django.urls import path

from features.authentication.api import views

urlpatterns = [
    path("", views.AuthenticateAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="login"),
    
]
