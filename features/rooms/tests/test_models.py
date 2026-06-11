import pytest
from features.rooms.models import Message, MESSAGE_LENGTH


@pytest.mark.django_db
def test_room_str_contains_name(room):
    assert room.name in str(room.name)


@pytest.mark.django_db
def test_room_created_by_is_set(room, user):
    assert room.created_by == user


@pytest.mark.django_db
def test_room_has_timestamps(room):
    assert room.created_at is not None
    assert room.updated_at is not None


@pytest.mark.django_db
def test_message_str(message, user):
    assert str(message) == f"{user.name} - {message.room.name}"


@pytest.mark.django_db
def test_message_body_is_stored(message):
    assert message.body == "Hello World"


@pytest.mark.django_db
def test_message_room_relation(message, room):
    assert message.room == room


@pytest.mark.django_db
def test_message_author_relation(message, user):
    assert message.author == user


@pytest.mark.django_db
def test_message_sended_at_is_set(message):
    assert message.sended_at is not None


@pytest.mark.django_db
def test_message_body_max_length():
    max_length = Message._meta.get_field("body").max_length
    assert max_length == MESSAGE_LENGTH


@pytest.mark.django_db
def test_room_messages_related_name(room, message):
    assert message in room.messages.all()


@pytest.mark.django_db
def test_deleting_room_cascades_to_messages(room, message):
    room.delete()
    assert Message.objects.filter(id=message.id).count() == 0
