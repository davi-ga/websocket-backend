from rest_framework import serializers
from features.users.api.serializers import UserSerializer


class AuthenticationSchema(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = UserSerializer()
