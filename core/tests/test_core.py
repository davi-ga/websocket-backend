import pytest
from django.http import HttpRequest
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication

from core.authentication import CsrfExemptSessionAuthentication


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
