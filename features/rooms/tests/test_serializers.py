import pytest
from features.rooms.api.serializers import (
    RoomRetrieveSerializer,
    RoomSerializer,
    MessageSerializer,
    MessageRetrieveSerializer,
)


@pytest.mark.django_db
def test_room_serializer_valid_data(authenticated_request):
    data = {"name": "New Room"}
    serializer = RoomSerializer(data=data, context={"request": authenticated_request})

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_room_serializer_missing_name_is_invalid(authenticated_request):
    serializer = RoomSerializer(data={}, context={"request": authenticated_request})

    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_room_serializer_created_by_is_hidden(authenticated_request):
    data = {"name": "New Room"}
    serializer = RoomSerializer(data=data, context={"request": authenticated_request})
    serializer.is_valid()
    room = serializer.save()

    assert room.created_by == authenticated_request.user


@pytest.mark.django_db
def test_room_retrieve_serializer_contains_messages(room, message, authenticated_request):
    serializer = RoomRetrieveSerializer(room, context={"request": authenticated_request})

    assert "messages" in serializer.data
    assert len(serializer.data["messages"]) == 1


@pytest.mark.django_db
def test_room_retrieve_serializer_created_by_is_nested(room, authenticated_request):
    serializer = RoomRetrieveSerializer(room, context={"request": authenticated_request})

    assert isinstance(serializer.data["created_by"], dict)
    assert "email" in serializer.data["created_by"]


@pytest.mark.django_db
def test_message_serializer_valid_data(room, authenticated_request):
    data = {"room": room.id, "body": "Hello World"}
    serializer = MessageSerializer(data=data, context={"request": authenticated_request})

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_message_serializer_missing_body_is_invalid(room, authenticated_request):
    data = {"room": room.id}
    serializer = MessageSerializer(data=data, context={"request": authenticated_request})

    assert not serializer.is_valid()
    assert "body" in serializer.errors


@pytest.mark.django_db
def test_message_serializer_author_is_hidden(room, authenticated_request):
    data = {"room": room.id, "body": "Hello World"}
    serializer = MessageSerializer(data=data, context={"request": authenticated_request})
    serializer.is_valid()
    message = serializer.save()

    assert message.author == authenticated_request.user


@pytest.mark.django_db
def test_message_serializer_room_is_write_only(message, authenticated_request):
    serializer = MessageSerializer(message, context={"request": authenticated_request})

    assert "room" not in serializer.data


@pytest.mark.django_db
def test_message_retrieve_serializer_author_is_nested(message, authenticated_request):
    serializer = MessageRetrieveSerializer(message, context={"request": authenticated_request})

    assert isinstance(serializer.data["author"], dict)
    assert "email" in serializer.data["author"]