import pytest
from django.urls import reverse

from features.users.models import User

LOGIN_URL = reverse("login")
LOGOUT_URL = reverse("logout")


@pytest.mark.django_db
def test_login_with_valid_credentials(client, user, user_payload):
    res = client.post(LOGIN_URL, {"email": user_payload["email"], "password": user_payload["password"]}, format="json")
    assert res.status_code == 200
    assert "success" in res.data


@pytest.mark.django_db
def test_login_with_invalid_password(client, user, user_payload):
    res = client.post(LOGIN_URL, {"email": user_payload["email"], "password": "wrong_password"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_login_with_nonexistent_email(client):
    res = client.post(LOGIN_URL, {"email": "nobody@example.com", "password": "secret"}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_login_with_missing_fields(client):
    res = client.post(LOGIN_URL, {}, format="json")
    assert res.status_code == 400
    assert "email" in res.data
    assert "password" in res.data


@pytest.mark.django_db
def test_login_with_invalid_email_format(client):
    res = client.post(LOGIN_URL, {"email": "not-an-email", "password": "secret"}, format="json")
    assert res.status_code == 400
    assert "email" in res.data


@pytest.mark.django_db
def test_login_with_inactive_user(client, user_payload):

    User.objects.create_user(**user_payload) 
    res = client.post(LOGIN_URL, {"email": user_payload["email"], "password": user_payload["password"]}, format="json")
    assert res.status_code == 400


@pytest.mark.django_db
def test_logout(client):
    res = client.post(LOGOUT_URL)
    assert res.status_code == 200
    assert "success" in res.data


@pytest.mark.django_db
def test_logout_clears_session(client, user, user_payload):
    client.post(LOGIN_URL, {"email": user_payload["email"], "password": user_payload["password"]}, format="json")
    res = client.post(LOGOUT_URL)
    assert res.status_code == 200
