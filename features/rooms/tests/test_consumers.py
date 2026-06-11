import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from channels.routing import URLRouter

from features.rooms.models import Message, Room, MESSAGE_LENGTH
from features.rooms.routing import ws_urlpatterns


async def make_communicator(user, room_id):
    communicator = WebsocketCommunicator(
        URLRouter(ws_urlpatterns),
        f"/room/{room_id}/chat/",
    )
    communicator.scope["user"] = user
    return communicator


@pytest.mark.django_db(transaction=True)
async def test_connect_authenticated_user(mock_user, mock_room):
    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        connected, _ = await communicator.connect()

        assert connected

        response = await communicator.receive_json_from()
        assert response["username"] == "system"
        assert "joined" in response["message"]

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_connect_anonymous_user(anonymous_user, mock_room):
    communicator = await make_communicator(anonymous_user, mock_room.id)
    connected, _ = await communicator.connect()

    assert not connected


@pytest.mark.django_db(transaction=True)
async def test_connect_room_not_found(mock_user):

    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(side_effect=Room.DoesNotExist),
    ):
        communicator = await make_communicator(mock_user, room_id=999)
        connected, _ = await communicator.connect()

        assert not connected


@pytest.mark.django_db(transaction=True)
async def test_disconnect_sends_system_message(mock_user, mock_room):
    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        await communicator.connect()
        await communicator.receive_json_from()

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_disconnect_message_received_by_other_client(mock_user, mock_second_user, mock_room):

    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        client1 = await make_communicator(mock_user, mock_room.id)
        client2 = await make_communicator(mock_second_user, mock_room.id)

        await client1.connect()
        await client1.receive_json_from()

        await client2.connect()
        await client2.receive_json_from()
        await client1.receive_json_from()

        await client1.disconnect()

        msg = await client2.receive_json_from()
        assert "disconnected" in msg["message"]
        assert msg["username"] == "system"

        await client2.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_receive_valid_message(mock_user, mock_room):
    with (
        patch(
            "features.rooms.consumers.ChatConsumer.get_room",
            new=AsyncMock(return_value=mock_room),
        ),
        patch(
            "features.rooms.consumers.ChatConsumer.save_message",
            new=AsyncMock(),
        ) as mock_save,
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        message = "Hello World!"
        await communicator.connect()
        await communicator.receive_json_from()

        await communicator.send_json_to({"message": message})

        response = await communicator.receive_json_from()
        assert response["message"] == message
        assert response["username"] == "TestUser"
        mock_save.assert_called_once_with(message)

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_receive_message_too_long_is_ignored(mock_user, mock_room):

    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        await communicator.connect()
        await communicator.receive_json_from()

        long_msg = "x" * (MESSAGE_LENGTH + 1)
        await communicator.send_json_to({"message": long_msg})

        assert await communicator.receive_nothing()

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_receive_empty_message_is_ignored(mock_user, mock_room):
    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        await communicator.connect()
        await communicator.receive_json_from()

        await communicator.send_json_to({"message": ""})

        assert await communicator.receive_nothing()

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_receive_null_text_data_is_ignored(mock_user, mock_room):
    with patch(
        "features.rooms.consumers.ChatConsumer.get_room",
        new=AsyncMock(return_value=mock_room),
    ):
        communicator = await make_communicator(mock_user, mock_room.id)
        await communicator.connect()
        await communicator.receive_json_from()

        await communicator.send_json_to({})

        assert await communicator.receive_nothing()

        await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_message_is_saved_to_database(user, room):

    communicator = await make_communicator(user, room.id)
    _, _ = await communicator.connect()
    await communicator.receive_json_from()

    await communicator.send_json_to({"message": "stored in database"})
    await communicator.receive_json_from()

    count = await database_sync_to_async(Message.objects.filter(body="stored in database").count)()
    assert count == 1

    await communicator.disconnect()


@pytest.mark.django_db(transaction=True)
async def test_message_broadcast_to_multiple_clients(mock_user, mock_second_user, mock_room):
    with (
        patch(
            "features.rooms.consumers.ChatConsumer.get_room",
            new=AsyncMock(return_value=mock_room),
        ),
        patch(
            "features.rooms.consumers.ChatConsumer.save_message",
            new=AsyncMock(),
        ),
    ):
        sender = await make_communicator(mock_user, mock_room.id)
        listener = await make_communicator(mock_second_user, mock_room.id)

        await sender.connect()
        await sender.receive_json_from()

        await listener.connect()
        await listener.receive_json_from()
        await sender.receive_json_from()

        await sender.send_json_to({"message": "broadcast test"})

        sender_msg = await sender.receive_json_from()
        listener_msg = await listener.receive_json_from()

        assert sender_msg["message"] == "broadcast test"
        assert listener_msg["message"] == "broadcast test"

        await sender.disconnect()
        await listener.disconnect()
