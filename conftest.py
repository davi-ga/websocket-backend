import pytest
from features.users.models import User
from rest_framework.test import APIClient


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
