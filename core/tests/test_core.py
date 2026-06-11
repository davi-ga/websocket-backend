import pytest
from django.http import HttpRequest
from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication

from core.authentication import CsrfExemptSessionAuthentication
from core.health.api.serializers import HealthCheckSerializer


def test_csrf_exempt_session_authentication():
    request = HttpRequest()
    request.method = "POST"

    custom_auth = CsrfExemptSessionAuthentication()

    try:
        result = custom_auth.enforce_csrf(request)
        assert result is None
    except Exception as e:
        pytest.fail(e)


def test_csrf_comparison_with_original_class():
    request = HttpRequest()
    request.method = "POST"

    original_auth = SessionAuthentication()

    with pytest.raises(PermissionDenied):
        original_auth.enforce_csrf(request)


def test_health_check_serializer():
    serializer = HealthCheckSerializer(data={"status": "ok"})
    assert serializer.is_valid()
    assert serializer.validated_data["status"] == "ok"


def test_health_check_view_returns_200(client):
    url = reverse("health_check")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK