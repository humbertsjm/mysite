from typing import Self

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.coreapp.models.currency import Currency


class ExchangeRatioManager(models.Manager):
    def new_ratio(
        self: Self,
        _from: Currency,
        _to: Currency,
        _ratio: float,
    ):
        return self.create(
            from_currency=_from
            ,to_currency=_to
            ,ratio=_ratio
        )


class ExchangeRatio(models.Model):
    id = models.AutoField(
        'id',
        primary_key=True,
    )
    from_currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name="from_currency",
        related_query_name="from_currency",
        help_text="From 1 custom unit",
    )
    to_currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
        related_name="to_currency",
        related_query_name="to_currency",
        help_text="To ratio system units",
    )
    ratio = models.DecimalField(
        'Ratio',
        null=False,
        blank=False,
        editable=True,
        max_digits=settings.DECIMAL_PLACES + 5,
        decimal_places=settings.DECIMAL_PLACES,
        default=0,
        help_text="How many [to_currency] are equivalent to 1 [from_currency]",
    )
    enabled_at = models.DateField(
        'Enabled at',
        null=True,
        blank=True,
        editable=False,
        auto_now_add=True,
    )
    disabled_at = models.DateField(
        'Deleted at',
        null=True,
        blank=True,
        editable=True,
    )

    objects = models.Manager()
    dbfunctions = ExchangeRatioManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "Exchange ratio"
        verbose_name_plural: str = "Exchange ratios"
        get_latest_by: str = "-enabled_at"
        ordering: list[str] = ["-enabled_at"]

    @property
    def pk(self: Self) -> int:
        return self.id

    @property
    def is_active(self: Self) -> bool:
        return self.disabled_at is None

    def __str__(self: Self) -> str:
        return '{}1 {} to {} {} | valid from {}'.format(
            '' if self.is_active else '(deprecated) ',
            self.from_currency.name,
            self.ratio,
            self.to_currency.name,
            self.enabled_at,
        )

    def save(self: Self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("exchange_ratio", kwargs={"pk": self.pk})
