import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_user_returns_201(client, user_payload):
    url = reverse("users-list")
    response = client.post(url, user_payload, format="json")

    assert response.status_code == 201
    assert response.data["email"] == user_payload["email"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_create_user_missing_fields_returns_400(client):
    url = reverse("users-list")
    response = client.post(url, {}, format="json")

    assert response.status_code == 400
    assert "email" in response.data
    assert "name" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_create_user_short_password_returns_400(client, user_payload):
    url = reverse("users-list")
    user_payload["password"] = "123"
    response = client.post(url, user_payload, format="json")

    assert response.status_code == 400
    assert "password" in response.data


@pytest.mark.django_db
def test_create_user_duplicate_email_returns_400(client, user, user_payload):
    url = reverse("users-list")
    response = client.post(url, user_payload, format="json")

    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
def test_me_authenticated_returns_200(authenticated_client, user, user_payload):
    url = reverse("me")
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == user_payload["email"]
    assert response.data["name"] == user_payload["name"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_me_anonymous_returns_403(client):
    url = reverse("me")
    response = client.get(url)

    assert response.status_code == 403
