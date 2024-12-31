import uuid as _uuid
from typing import Self

from django.conf import settings
from django.db import models
from django.urls import reverse

from apps.accounting.models.accounting_behavior import AccountingBehavior
from apps.coreapp.enums import DEFAULT_FOLIO
from apps.coreapp.models.currency import Currency
from apps.coreapp.models.entity import Entity
from apps.coreapp.models.profile import Profile


class AccountManager(models.Manager):
    def new_account(
        self: Self,
        _label: str,
        _owner: Profile,
        _entity: Entity,
        _behavior: AccountingBehavior,
        _currency: Currency,
        *,
        _folio=DEFAULT_FOLIO,
        _reference: str = '',
        _quantity: float = 0,
    ):
        return self.create(
            label=_label,
            owner=_owner,
            entity=_entity,
            behavior=_behavior,
            currency=_currency,
            folio=_folio,
            reference=_reference,
            quantity=_quantity,
        )

    def get_by_behavior(
        self: Self,
        _behavior: AccountingBehavior,
    ):
        return self.all().filter(behavior=_behavior).order_by('folio')

class Account(models.Model):
    uuid = models.UUIDField(
        'UUID',
        primary_key=True,
        default=_uuid.uuid4,
    )
    label = models.CharField(
        'Label',
        null=False,
        blank=False,
        editable=True,
        max_length=50,
    )
    owner = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        null=True,
    )
    behavior = models.ForeignKey(
        AccountingBehavior,
        on_delete=models.SET_NULL,
        null=True,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.SET_NULL,
        null=True,
    )
    folio = models.PositiveSmallIntegerField(
        'Folio',
        null=False,
        blank=True,
        editable=True,
        default=DEFAULT_FOLIO,
        help_text='Order in reports and most displays',
    )
    reference = models.CharField(
        'Reference',
        null=False,
        blank=True,
        editable=True,
        max_length=50,
    )
    quantity = models.DecimalField(
        'Quantity',
        null=False,
        blank=True,
        editable=False,
        max_digits=settings.DECIMAL_PLACES + 7,
        decimal_places=settings.DECIMAL_PLACES,
        default=0,
    )
    created_at = models.DateTimeField(
        'Created at',
        null=False,
        blank=True,
        editable=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        'Updated at',
        null=True,
        blank=True,
        editable=False,
        auto_now=True,
    )
    deleted_at = models.DateField(
        'Deleted at',
        null=True,
        blank=True,
        editable=True,
    )

    objects = models.Manager()
    dbfunctions = AccountManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "Account"
        verbose_name_plural: str = "Accounts"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["owner__name", "folio"]

    @property
    def pk(self) -> _uuid.UUID:
        return self.uuid

    @property
    def is_active(self) -> bool:
        return self.deleted_at is not None

    def __str__(self) -> str:
        return '{} {} = {} {}'.format(
            str(self.folio).zfill(3),
            self.label,
            self.quantity,
            self.currency.name,
        )

    def save(self, *args, **kwargs) -> None:
        self.label: str = self.label.strip()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("account", kwargs={"pk": self.pk})

    def deposit(self, _quantity) -> None:
        self.quantity += _quantity
        # if self.tag in [x.value for x in self.DEBITABLE_ACCOUNTS]:
        #     self.quantity += _quantity
        # elif self.tag in [x.value for x in self.CREDITABLE_ACCOUNTS]:
        #     self.quantity -= _quantity
        # else:
        #     raise ValueError("Account tag not supported")

    def withdraw(self, _quantity) -> None:
        self.quantity -= _quantity
        # if self.tag in [x.value for x in self.DEBITABLE_ACCOUNTS]:
        #     self.quantity -= _quantity
        # elif self.tag in [x.value for x in self.CREDITABLE_ACCOUNTS]:
        #     self.quantity += _quantity
        # else:
        #     raise ValueError("Account tag not supported")
