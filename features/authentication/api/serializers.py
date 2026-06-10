from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers


class AuthenticateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(self.context.get("request"), username=email, password=password)

        if user is None:
            raise serializers.ValidationError({"detail": "Invalid email or password"})

        attrs["user"] = user

        update_last_login(None, user)

        return attrs
