import pytest
from rest_framework.test import APIClient, APIRequestFactory
from unittest.mock import MagicMock

from features.users.models import User
from features.rooms.models import Message, Room

from core.asgi import application


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_payload():
    return {"name": "Davi", "email": "contato@daviga.dev.br", "password": "senha_segura_123"}


@pytest.fixture
def user(db, user_payload):
    return User.objects.create_user(**user_payload, is_active=True)


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def room(db, user):
    return Room.objects.create(name="Test Room", created_by=user)


@pytest.fixture
def message(room, user):
    return Message.objects.create(room=room, author=user, body="Hello World")


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def authenticated_request(request_factory, user):
    request = request_factory.get("/")
    request.user = user
    return request


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.is_authenticated = True
    user.name = "TestUser"
    return user


@pytest.fixture
def mock_room():
    room = MagicMock()
    room.id = 1
    return room


@pytest.fixture
def anonymous_user():
    user = MagicMock()
    user.is_authenticated = False
    return user


@pytest.fixture
def mock_second_user():
    second_user = MagicMock()
    second_user.is_authenticated = True
    second_user.name = "SecondUser"
