from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from features.users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "name", "is_staff", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2"),
        }),
    )
    search_fields = ("email", "name")