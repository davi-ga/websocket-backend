import json
from typing import Literal
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from features.rooms.models import Room, Message, MESSAGE_LENGTH
from features.users.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.room: Room | None = None
        self.room_group: str | None = None
        self.user: User | None = None

    async def connect(self) -> None:

        self.user = self.scope["user"]

        if self.user.is_authenticated:
            room_id = self.scope["url_route"]["kwargs"]["id"]

            try:
                self.room = await self.get_room(room_id)
            except Room.DoesNotExist:
                await self.close()
                return

            self.room_group = f"room_{self.room.id}"

            await self.channel_layer.group_add(self.room_group, self.channel_name)

            await self.accept()
            await self.send_system_message("join")

        else:
            await self.close()

    async def disconnect(self, code: int) -> None:
        if self.room_group and self.user and self.user.is_authenticated:
            await self.send_system_message("disconnect")
            await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data: str | None = None, bytes_data: bytes | None = None) -> None:
        if text_data is None:
            return

        data = json.loads(text_data)

        if data:
            message = data.get("message")

            if not message or len(message) > MESSAGE_LENGTH:
                return

            await self.channel_layer.group_send(
                self.room_group,
                {
                    "type": "chat_message",
                    "username": self.user.name,
                    "message": message,
                },
            )

            await self.save_message(message)

        else:
            return

    async def chat_message(self, event: dict[str, str]) -> None:
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                }
            )
        )

    async def send_system_message(self, message_type: Literal["join", "disconnect"]) -> None:

        messages = {
            "join": f"{self.user.name} joined the room",
            "disconnect": f"{self.user.name} disconnected from the room",
        }

        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "username": "system",
                "message": messages.get(message_type, f"{self.user.name} performed an action"),
            },
        )

    @database_sync_to_async
    def save_message(self, message: str) -> None:
        Message.objects.create(room=self.room, author=self.user, body=message)

    @database_sync_to_async
    def get_room(self, room_id: int) -> Room:
        return Room.objects.get(id=room_id)
