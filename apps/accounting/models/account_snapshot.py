from typing import Self

from django.db import models
from django.urls import reverse

from apps.accounting.models.account import Account
from apps.coreapp.enums import MonthOptionWithInitial


class AccountSnapshotManager(models.Manager):
    def new_snapshot(
        self: Self,
    ):
        pass


class AccountSnapshot(models.Model):
    id = models.BigAutoField(
        "Id",
        primary_key=True,
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
    )
    year = models.PositiveSmallIntegerField(
        'Year',
        null=False,
        blank=False,
        editable=True,
    )
    month = models.PositiveSmallIntegerField(
        'Month',
        choices=MonthOptionWithInitial,
        default=MonthOptionWithInitial.INI,
    )
    version = models.PositiveSmallIntegerField(
        'Version',
        null=False,
        blank=False,
        editable=True,
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
    dbfunctions = AccountSnapshotManager()

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
        return "{}-{} {}".format(
            self.year,
            self.month,
            self.account,
        )

    def save(self: Self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("account_snapshot", kwargs={"pk": self.pk})
