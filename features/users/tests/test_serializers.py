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
def test_password_min_length_validation():
    data = {"name": "Test User", "email": "short@example.com", "password": "123"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors


@pytest.mark.django_db
def test_valid_data_creates_user():
    data = {"name": "Test User", "email": "test@example.com", "password": "secret123"}
    serializer = UserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.pk is not None
    assert user.is_active is True


@pytest.mark.django_db
def test_password_is_hashed_on_create():
    data = {"name": "Test User", "email": "hash@example.com", "password": "secret123"}
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    assert user.password != "secret123"
    assert user.check_password("secret123")


def test_duplicate_email_is_invalid(user):
    data = {"name": "Outro", "email": user.email, "password": "secret123"}
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert "email" in serializer.errors
