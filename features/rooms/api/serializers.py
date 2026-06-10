from rest_framework import serializers

from features.rooms.models import Room, Message
from features.rooms.fields import CurrentUserDefault
from features.users.api.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):

    created_by = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Room
        fields = "__all__"
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class MessageSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Message
        fields = "__all__"
        extra_kwargs = {"sended_at": {"read_only": True}, "room": {"write_only": True}}


class MessageRetrieveSerializer(MessageSerializer):

    author = UserSerializer()


class RoomRetrieveSerializer(RoomSerializer):

    created_by = UserSerializer()
    messages = MessageRetrieveSerializer(many=True)


