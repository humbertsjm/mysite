from typing import Self

from django.db import models
from django.urls import reverse

from apps.coreapp.enums import DEFAULT_DISPLAY_ORDER, CurrencyTag


class CurrencyManager(models.Manager):
    def new_currency(
        self: Self,
        _name: str,
        _label: str,
        _tag: CurrencyTag,
        *,
        _display_order: int = DEFAULT_DISPLAY_ORDER,
    ):
        return self.create(
            name=_name, label=_label, tag=_tag, display_order=_display_order
        )

class Currency(models.Model):
    id = models.AutoField("id", primary_key=True)
    name = models.CharField(
        "Name",
        null=False,
        blank=False,
        editable=True,
        unique=True,
        max_length=10,
    )
    label = models.CharField(
        "Label",
        null=False,
        blank=False,
        editable=True,
        max_length=20,
    )
    tag = models.PositiveSmallIntegerField(
        "Currency tag",
        choices=CurrencyTag,
        default=CurrencyTag.MONEY,
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
    dbfunctions = CurrencyManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "currency"
        verbose_name_plural: str = "currencies"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["display_order"]

    @property
    def pk(self) -> int:
        return self.id

    def __str__(self) -> str:
        return "{}".format(self.label)

    def save(self, *args, **kwargs) -> None:
        self.name: str = self.name.strip().lower()
        self.name = self.name.replace(' ', '_')
        self.name = self.name.replace('-', '_')
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("currency", kwargs={"pk": self.pk})
