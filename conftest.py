import pytest
from features.users.models import User

@pytest.fixture
def user_payload():
    return {"name": "Davi", "email": "contato@daviga.dev.br", "password": "senha_segura_123"}


@pytest.fixture
def user(db, user_payload):
    return User.objects.create_user(**user_payload)