from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    @classmethod
    def custom_normalize_email(cls, email):

        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name.lower() + "@" + domain_part.lower()
        return email

    def _create_user(self, email: str | None = None, password: str | None = None, **extra_fields) -> AbstractBaseUser:

        email = self.custom_normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email: str | None = None, password: str | None = None, **extra_fields) -> AbstractBaseUser:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self, email: str | None = None, password: str | None = None, **extra_fields
    ) -> AbstractBaseUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self._create_user(email, password, **extra_fields)
