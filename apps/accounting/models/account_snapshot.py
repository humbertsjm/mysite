from typing import Self

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.accounting.models.account import Account
from apps.coreapp.enums import MonthOptionWithInitial


class AccountSnapshotManager(models.Manager):
    def new_snapshot(
        self: Self,
    ):
        pass

    def get_next_version(
            self: Self,
            _account: Account,
            _year: int,
            _month: int
        ) -> int:
        items = self.objects.all().filter(
            account=_account,
            year=_year,
            month=_month
        ).order_by("-version")
        if len(items) > 0:
            return int(items.first().value)
        return 1


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
        editable=False,
        default=1
    )
    current_quantity = models.DecimalField(
        'Current quantity',
        null=False,
        blank=True,
        editable=False,
        max_digits=settings.DECIMAL_PLACES + 7,
        decimal_places=settings.DECIMAL_PLACES,
        default=0,
    )
    audited_quantity = models.DecimalField(
        'Audited quantity',
        null=False,
        blank=False,
        editable=True,
        max_digits=settings.DECIMAL_PLACES + 7,
        decimal_places=settings.DECIMAL_PLACES,
        default=0,
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
        verbose_name: str = "Account snapshot"
        verbose_name_plural: str = "Account snapshots"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["-year", "-month", "-version"]

    @property
    def pk(self: Self) -> int:
        return self.id

    @property
    def is_active(self: Self) -> bool:
        return self.disabled_at is None

    @property
    def discrepancy(self: Self) -> float:
        return float(self.audited_quantity) - float(self.current_quantity)

    def __str__(self: Self) -> str:
        return "{}-{} {} > {} {} v{}".format(
            self.year,
            self.month,
            self.account.label,  # pylint: disable=E1101
            self.discrepancy,
            self.account.currency.label,  # pylint: disable=E1101
            self.version,
        )

    def save(self: Self, *args, **kwargs) -> None:
        self.current_quantity = self.account.quantity  # pylint: disable=E1101
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("account_snapshot", kwargs={"pk": self.pk})
