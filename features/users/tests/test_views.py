import pytest
from django.urls import reverse

USERS_LIST_URL = reverse("users-list")
ME_URL = reverse("me")


@pytest.mark.django_db
def test_create_user(client, user_payload):

    response = client.post(USERS_LIST_URL, user_payload, format="json")

    assert response.status_code == 201
    assert response.data["email"] == user_payload["email"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_create_user_missing_fields(client):

    response = client.post(USERS_LIST_URL, {}, format="json")

    assert response.status_code == 400
    assert "email" in response.data
    assert "name" in response.data
    assert "password" in response.data


@pytest.mark.django_db
def test_create_user_short_password(client, user_payload):

    user_payload["password"] = "123"
    response = client.post(USERS_LIST_URL, user_payload, format="json")

    assert response.status_code == 400
    assert "password" in response.data


@pytest.mark.django_db
def test_create_user_duplicate_email(client, user, user_payload):

    response = client.post(USERS_LIST_URL, user_payload, format="json")

    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
def test_me_authenticated(authenticated_client, user, user_payload):

    response = authenticated_client.get(ME_URL)

    assert response.status_code == 200
    assert response.data["email"] == user_payload["email"]
    assert response.data["name"] == user_payload["name"]
    assert "password" not in response.data


@pytest.mark.django_db
def test_me_anonymous(client):

    response = client.get(ME_URL)

    assert response.status_code == 403
