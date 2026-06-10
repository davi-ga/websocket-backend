from rest_framework import serializers


class SuccessResponseSchema(serializers.Serializer):

    success = serializers.CharField()
