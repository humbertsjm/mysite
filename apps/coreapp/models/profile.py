import uuid as _uuid
from typing import Self

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.coreapp.enums import DEFAULT_DISPLAY_ORDER


class ProfileManager(models.Manager):
    def new_profile(
        self: Self,
        _name: str,
        _label: str,
        _owner,
        *,
        _display_order: int = DEFAULT_DISPLAY_ORDER,
    ):
        return self.create(
            name=_name,
            label=_label,
            owner=_owner,
            display_order=_display_order,
        )

    def get_user_active_profile(self: Self, _user_id: int):
        user_profiles = self.all().filter(
            owner__id=_user_id, is_selected=True
        )
        if len(user_profiles) == 1:
            return user_profiles[0]

        if len(user_profiles) == 0:
            first_profile = self.all().filter(owner__id=_user_id).first()
            first_profile.is_selected = True
            first_profile.save()
            return first_profile

        return self.all().filter(owner__id=_user_id).first()

    def get_user_profiles(self: Self, _user_id: int):
        return self.all().filter(owner__id=_user_id)


class Profile(models.Model):
    uuid = models.UUIDField(
        "UUID",
        primary_key=True,
        default=_uuid.uuid4,
    )
    name = models.CharField(
        "Name",
        null=False,
        blank=False,
        editable=True,
        max_length=10,
    )
    label = models.CharField(
        "Label",
        null=False,
        blank=False,
        editable=True,
        max_length=30,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
    )
    is_selected = models.BooleanField(
        "Is selected",
        null=False,
        blank=True,
        editable=True,
        default=False,
        help_text="Profile currently active per user",
    )
    display_order = models.PositiveSmallIntegerField(
        "Display order",
        null=False,
        blank=True,
        editable=True,
        default=DEFAULT_DISPLAY_ORDER,
        help_text="Order in reports and most displays",
    )
    created_at = models.DateTimeField(
        "Created at",
        null=False,
        blank=True,
        editable=False,
        auto_now_add=True,
    )

    objects = models.Manager()
    dbfunctions = ProfileManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "profile"
        verbose_name_plural: str = "profiles"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["owner__username", "display_order"]

    @property
    def pk(self: Self) -> _uuid.UUID:
        return self.uuid

    def __str__(self: Self) -> str:
        return "{} -> {}".format(
            self.label,
            self.owner.username  # pylint: disable=E1101
        )

    def save(self: Self, *args, **kwargs) -> None:
        self.name: str = self.name.strip().lower()
        self.name = self.name.replace(' ', '_')
        self.name = self.name.replace('-', '_')
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("profile", kwargs={"pk": self.pk})
