import pytest
from features.users.api.serializers import UserSerializer
from features.users.models import User


@pytest.mark.django_db
def test_create_common_user_successfully(user_payload):

    user = User.objects.create_user(**user_payload)
    payload_password = user_payload.get("password")

    assert user.password is not None
    assert user.password != payload_password
    assert user.check_password(payload_password) is True

    assert user.is_staff is False
    assert user.is_active is False
    assert user.is_superuser is False

    assert user.last_login is None

    assert UserSerializer().fields["password"].write_only is True
