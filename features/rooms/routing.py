from django.urls import path

from features.rooms.consumers import ChatConsumer

ws_urlpatterns = [
    path("room/<int:id>/chat/", ChatConsumer.as_asgi()),
]
