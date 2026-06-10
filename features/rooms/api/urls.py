from django.urls import path, include
from rest_framework import routers

from features.rooms.consumers import ChatConsumer
from features.rooms.api import viewsets

room_router = routers.SimpleRouter()
room_router.register("", viewsets.RoomViewset, basename="rooms")

urlpatterns = [
    path("", include(room_router.urls)),
]

ws_urlpatterns = [
    path("room/<int:id>/chat/", ChatConsumer.as_asgi()),
]
