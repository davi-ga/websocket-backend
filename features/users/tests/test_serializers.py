import pytest
from features.users.api.serializers import UserSerializer


def test_write_only_fields():
    assert UserSerializer().fields["password"].write_only is True


def test_read_only_fields():
    fields = UserSerializer().fields
    assert fields["created_at"].read_only is True
    assert fields["updated_at"].read_only is True
    assert fields["last_login"].read_only is True
    assert fields["is_active"].read_only is True


def test_excluded_fields():
    fields = UserSerializer().fields
    assert "groups" not in fields
    assert "user_permissions" not in fields
    assert "is_staff" not in fields
    assert "is_superuser" not in fields


def test_missing_required_fields():
    serializer = UserSerializer(data={})
    assert not serializer.is_valid()
    assert "email" in serializer.errors
    assert "name" in serializer.errors
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_password_min_length_validation(user_payload):
    user_payload["password"] = "123"
    serializer = UserSerializer(data=user_payload)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_valid_data_creates_user(user_payload):
    serializer = UserSerializer(data=user_payload)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.id is not None
    assert user.is_active is True


@pytest.mark.django_db
def test_password_is_hashed_on_create(user_payload):
    serializer = UserSerializer(data=user_payload)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    assert user.password != user_payload["password"]
    assert user.check_password(user_payload["password"])


def test_duplicate_email_is_invalid(user, user_payload):
    serializer = UserSerializer(data=user_payload)
    assert not serializer.is_valid()
    assert "email" in serializer.errors
