import pytest
from features.authentication.api.serializers import AuthenticateSerializer


def test_required_fields():
    serializer = AuthenticateSerializer(data={})
    assert not serializer.is_valid()
    assert "email" in serializer.errors
    assert "password" in serializer.errors


def test_email_field_format():
    serializer = AuthenticateSerializer(data={"email": "not-an-email", "password": "secret123"})
    assert not serializer.is_valid()
    assert "email" in serializer.errors


@pytest.mark.django_db
def test_valid_credentials(user, user_payload):
    data = {"email": user_payload["email"], "password": user_payload["password"]}
    serializer = AuthenticateSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["user"] == user


@pytest.mark.django_db
def test_invalid_password_raises_error(user, user_payload):
    data = {"email": user_payload["email"], "password": "wrong_password"}
    serializer = AuthenticateSerializer(data=data)
    assert not serializer.is_valid()
    assert "non_field_errors" in serializer.errors or "detail" in str(serializer.errors)


@pytest.mark.django_db
def test_nonexistent_email_raises_error():
    data = {"email": "nobody@example.com", "password": "secret123"}
    serializer = AuthenticateSerializer(data=data)
    assert not serializer.is_valid()


@pytest.mark.django_db
def test_last_login_is_updated(user, user_payload):
    assert user.last_login is None
    data = {"email": user_payload["email"], "password": user_payload["password"]}
    serializer = AuthenticateSerializer(data=data)
    serializer.is_valid()
    user.refresh_from_db()
    assert user.last_login is not None


@pytest.mark.django_db
def test_inactive_user_cannot_authenticate(user_payload):
    from features.users.models import User

    inactive_user = User.objects.create_user(**user_payload)
    # is_active=False por padrão no create_user
    data = {"email": user_payload["email"], "password": user_payload["password"]}
    serializer = AuthenticateSerializer(data=data)
    assert not serializer.is_valid()
