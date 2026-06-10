from rest_framework import serializers
from django.core.validators import MinLengthValidator
from features.users.models import User


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, validators=[MinLengthValidator(6)])

    class Meta:
        model = User
        exclude = ["groups", "user_permissions", "is_staff", "is_superuser"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "last_login": {"read_only": True},
            "is_active": {"read_only": True},
        }

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(email=email, password=password, **validated_data)
        user.is_active = True
        user.save()

        return user
