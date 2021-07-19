from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver, Signal
from django.utils.html import mark_safe
from django.utils.translation import ugettext as _


from apps.common import models as common_models


class User(PermissionsMixin, AbstractBaseUser, common_models.AbstractBaseModel):
    username_validator = UnicodeUsernameValidator()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    email = models.EmailField("Email address", blank=True)
    is_active = models.BooleanField("Active", default=True)
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    full_name = models.CharField(max_length=80, null=True, blank=True)
    username = models.CharField(
        "Username", max_length=255, unique=True, validators=[username_validator]
    )

    objects = UserManager()

    class Meta:
        ordering = [
            "username",
            "full_name",
        ]

    def __str__(self):
        return f"{self.username}"


class Settings(common_models.AbstractBaseModel):
    """Settings for individual User"""

    USER_ROLES = (
        ("MEMBER", "Member"),
        ("FARM_ADMIN", "Farm Admin"),
        ("FARM_USER", "Farm User"),
        ("ADMIN", "Platform Admin"),
    )

    avatar = models.ImageField(
        upload_to="avatars",
        default="../static/img/avatars/default-user-avatar.png",
        null=True,
        blank=True,
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default="MEMBER")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return f"{self.user} | settings"

    class Meta:
        verbose_name_plural = "Settings"


@receiver(post_save, sender=User)
def create_user_settings_on_superuser_creation(sender, created, instance, **kwargs):
    """
    Create settings(User) upon Superuser instance creation
    - Other users will be created via API calling service, not signal
    """
    from apps.users.models import Settings

    if created and User.is_superuser:
        Settings.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_all_apps_settings_on_superuser_creation(sender, created, instance, **kwargs):
    """Create settings per app for all relevant CSADemo project apps upon initial user creation"""
    from django.apps import registry

    if created and User.is_superuser and User.objects.all().count() == 1:
        for app in settings.PROJECT_APPS:
            APPS_WITHOUT_SETTINGS = ["apps.common", "apps.api", "apps.users"]
            if app in APPS_WITHOUT_SETTINGS:
                continue
            app_label = app.split(".")[1]
            try:
                settings_model = registry.apps.get_model(app_label, "Settings")
            except LookupError:
                continue
            if settings_model.objects.all().count() == 0:
                settings_model.objects.create()
        return
    else:
        return
