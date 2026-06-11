import pytest
from django.urls import reverse

ROOMS_LIST_URL = reverse("rooms-list")


@pytest.mark.django_db
def test_create_room_authenticated(authenticated_client):
    response = authenticated_client.post(ROOMS_LIST_URL, {"name": "New Room"}, format="json")

    assert response.status_code == 201
    assert response.data["name"] == "New Room"


@pytest.mark.django_db
def test_create_room_anonymous(client):
    response = client.post(ROOMS_LIST_URL, {"name": "New Room"}, format="json")

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_room_missing_name(authenticated_client):
    response = authenticated_client.post(ROOMS_LIST_URL, {}, format="json")

    assert response.status_code == 400
    assert "name" in response.data


@pytest.mark.django_db
def test_list_rooms_authenticated(authenticated_client, room):
    response = authenticated_client.get(ROOMS_LIST_URL)

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_list_rooms_anonymous(client):
    response = client.get(ROOMS_LIST_URL)

    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_room_authenticated(authenticated_client, room, message):
    url = reverse("rooms-detail", args=[room.pk])
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == room.name
    assert "messages" in response.data
    assert len(response.data["messages"]) == 1


@pytest.mark.django_db
def test_retrieve_room_anonymous(client, room):
    url = reverse("rooms-detail", args=[room.pk])
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_room_not_found(authenticated_client):
    url = reverse("rooms-detail", args=[9999])
    response = authenticated_client.get(url)

    assert response.status_code == 404
