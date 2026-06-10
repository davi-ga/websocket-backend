from rest_framework import viewsets, mixins
from features.rooms.api.serializers import RoomRetrieveSerializer, RoomSerializer
from features.rooms.models import Room


class RoomViewset(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):

    serializer_class = RoomSerializer
    queryset = Room.objects.all().select_related("created_by")

    def get_serializer_class(self):

        if self.action in ["retrieve"]:
            return RoomRetrieveSerializer

        return super().get_serializer_class()
