from typing import Self

from django.db import models
from django.urls import reverse

from apps.coreapp.enums import DEFAULT_DISPLAY_ORDER, EntityTag


class EntityManager(models.Manager):
    def new_entity(
        self: Self,
        _name: str,
        _label: str,
        _tag: EntityTag,
        *,
        _display_order: int = DEFAULT_DISPLAY_ORDER,
    ) :
        return self.create(
            name=_name,
            label=_label,
            tag=_tag,
            display_order=_display_order,
        )


class Entity(models.Model):
    id = models.AutoField(
        "id",
        primary_key=True,
    )
    name = models.CharField(
        "Name",
        null=False,
        blank=False,
        editable=True,
        unique=True,
        max_length=20,
    )
    label = models.CharField(
        "Name",
        null=False,
        blank=False,
        editable=True,
        max_length=50,
    )
    tag = models.PositiveSmallIntegerField(
        "Entity tag",
        choices=EntityTag,
        default=EntityTag.BANK,
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
    disabled_at = models.DateField(
        "Deleted at",
        null=True,
        blank=True,
        editable=True,
    )

    objects = models.Manager()
    dbfunctions = EntityManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "entity"
        verbose_name_plural: str = "entities"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["display_order"]

    @property
    def pk(self: Self) -> int:
        return self.id

    @property
    def is_active(self: Self) -> bool:
        return self.disabled_at is None

    def __str__(self: Self) -> str:
        return "{} - {}".format(
            self.label,
            EntityTag.get_label(self.tag)
        )

    def save(self: Self, *args, **kwargs) -> None:
        self.name: str = self.name.strip().lower()
        self.name = self.name.replace(' ', '_')
        self.name = self.name.replace('-', '_')
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("entity", kwargs={"pk": self.pk})
