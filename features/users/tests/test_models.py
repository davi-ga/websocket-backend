import pytest
from features.users.models import User
from django.db.utils import IntegrityError


@pytest.mark.django_db
def test_create_user_stores_fields(db, user_payload):
    user = User.objects.create_user(**user_payload)

    assert user.id is not None
    assert user.name == user_payload["name"]
    assert user.email == user_payload["email"]


@pytest.mark.django_db
def test_create_user_hashes_password(db, user_payload):
    user = User.objects.create_user(**user_payload)

    assert user.password != user_payload["password"]
    assert user.check_password(user_payload["password"]) is True


@pytest.mark.django_db
def test_create_user_default_flags(db, user_payload):
    user = User.objects.create_user(**user_payload)

    assert user.is_staff is False
    assert user.is_active is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_last_login_is_none(db, user_payload):
    user = User.objects.create_user(**user_payload)

    assert user.last_login is None


@pytest.mark.django_db
def test_create_superuser_flags_are_true(db, user_payload):
    user = User.objects.create_superuser(**user_payload)

    assert user.is_staff is True
    assert user.is_active is True
    assert user.is_superuser is True


@pytest.mark.django_db
def test_create_superuser_last_login_is_none(db, user_payload):
    user = User.objects.create_superuser(**user_payload)

    assert user.last_login is None


@pytest.mark.django_db
def test_duplicate_email_raises_integrity_error(user, user_payload):
    with pytest.raises(IntegrityError):
        User.objects.create_user(**user_payload)


@pytest.mark.django_db
def test_email_is_normalized(db, user_payload):
    email = user_payload.pop("email")
    user = User.objects.create_user(email=email.upper(), **user_payload)

    assert user.email == email


@pytest.mark.django_db
def test_user_has_timestamps(user):
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.django_db
def test_str_is_email(user, user_payload):
    assert str(user) == user_payload["email"]
