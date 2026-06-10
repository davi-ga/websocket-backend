from django.db import models
from django.utils.translation import gettext_lazy as _

MESSAGE_LENGTH = 250


class Room(models.Model):

    name = models.CharField(_("Name"), max_length=50)

    created_by = models.ForeignKey("users.User", verbose_name=_("Created by"), on_delete=models.PROTECT)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class Message(models.Model):

    room = models.ForeignKey("rooms.Room", verbose_name=_("Room"), related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", verbose_name=_("Author"), on_delete=models.PROTECT)

    body = models.CharField(_("Body"), max_length=MESSAGE_LENGTH)

    sended_at = models.DateTimeField(_("Sended At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        indexes = [models.Index(fields=["author", "room"])]
