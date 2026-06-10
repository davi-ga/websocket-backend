from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from features.users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(_("Name"), max_length=50)
    email = models.CharField(_("Email"), max_length=50, unique=True)
    password = models.CharField(_(""), max_length=128)

    is_active = models.BooleanField(_("Is Active?"), default=False)
    is_staff = models.BooleanField(_("Is Staff?"), default=False)

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    last_login = models.DateTimeField(_("Last Login"), null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    PASSWORD_FIELD = "password"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
