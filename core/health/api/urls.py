from django.urls import path
from .views import HealthAPIView

urlpatterns = [
    path("", HealthAPIView.as_view(), name="health_check"),
]
