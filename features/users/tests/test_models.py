import pytest
from datetime import timedelta
from features.users.models import User
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_create_user_successfully(user_payload):

    user = User.objects.create_user(**user_payload)
    payload_password = user_payload["password"]

    assert user.id is not None
    assert user.name == user_payload["name"]
    assert user.email == user_payload["email"]

    assert user.password is not None
    assert user.password != payload_password
    assert user.check_password(payload_password) is True

    assert user.is_staff is False
    assert user.is_active is False
    assert user.is_superuser is False

    assert user.last_login is None


@pytest.mark.django_db
def test_create_superuser_successfully(user_payload):

    user = User.objects.create_superuser(**user_payload)

    assert user.id is not None
    assert user.is_staff is True
    assert user.is_active is True
    assert user.is_superuser is True

    assert user.last_login is None


@pytest.mark.django_db
def test_duplicate_email(user, user_payload):
    with pytest.raises(IntegrityError):
        User.objects.create_user(**user_payload)


@pytest.mark.django_db
def test_custom_email_normalize(user_payload):
    email = user_payload.pop("email")

    user = User.objects.create_user(email=email.upper(), **user_payload)

    assert user.email == email


@pytest.mark.django_db
def test_date_field_autofill(user):

    assert user.created_at is not None
    assert user.updated_at is not None
    assert abs(user.updated_at - user.created_at) < timedelta(seconds=1)


@pytest.mark.django_db
def test_str_representation(user, user_payload):

    assert str(user) == user_payload["email"]
