from typing import Self

from django.db import models
from django.urls import reverse

from apps.coreapp.enums import DEFAULT_FOLIO, AccountingCategoryTag


class AccountingBehaviorManager(models.Manager):
    def new_accounting_behavior(
        self: Self,
        _tag: AccountingCategoryTag,
        _folio: int,
        _name: str,
        _label: str,
        *,
        _is_physical_cash: bool=False,
        _is_digital_cash: bool=False,
        _is_physical_item: bool=False,
        _is_payment_method: bool=False,
        _is_formal_payable: bool=False,
        _is_informal_payable: bool=False,
        _is_property_associated: bool=False,
    ):
        return self.create(
            tag=_tag,
            folio=_folio,
            name=_name,
            label=_label,
            is_physical_cash=_is_physical_cash,
            is_digital_cash=_is_digital_cash,
            is_physical_item=_is_physical_item,
            is_payment_method=_is_payment_method,
            is_formal_payable=_is_formal_payable,
            is_informal_payable=_is_informal_payable,
            is_property_associated=_is_property_associated,
        )

    def get_by_tag(
        self: Self,
        _tag: AccountingCategoryTag,
    ):
        return self.all().filter(tag=_tag).order_by('folio')


class AccountingBehavior(models.Model):
    id = models.AutoField(
        'id',
        primary_key=True,
    )
    tag = models.PositiveSmallIntegerField(
        'Tag',
        choices=AccountingCategoryTag,
        default=AccountingCategoryTag.ASSET,
    )
    folio = models.PositiveSmallIntegerField(
        'Folio',
        null=False,
        blank=True,
        editable=True,
        default=DEFAULT_FOLIO,
        help_text='Order in reports and most displays',
    )
    name = models.CharField(
        'Name',
        null=False,
        blank=False,
        editable=True,
        unique=True,
        max_length=30,
    )
    label = models.CharField(
        'Label',
        null=False,
        blank=False,
        editable=True,
        max_length=50,
    )
    is_physical_cash = models.BooleanField(
        'Is cash',
        null=False,
        blank=True,
        editable=True,
        default=False,
        help_text="Physical cash or cash equivalents",
    )
    is_digital_cash = models.BooleanField(
        'Is digital cash',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Is cash representd by an account with a third party entity',
    )
    is_physical_item = models.BooleanField(
        'Is physical cash',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Is non-cash object or item with a stable cash equivalent',
    )
    is_payment_method = models.BooleanField(
        'Is payment method',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Can be used as payment method',
    )
    is_formal_payable = models.BooleanField(
        'Is payment method',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Represent a formal debt between parties',
    )
    is_informal_payable = models.BooleanField(
        'Is payment method',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Represent an informal debt between parties',
    )
    is_property_associated = models.BooleanField(
        'Is property associated',
        null=False,
        blank=True,
        editable=True,
        default=True,
        help_text='Represent an informal debt between parties',
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
    deprecated_at = models.DateField(
        'Deprecated at',
        null=True,
        blank=True,
        editable=True,
    )

    objects = models.Manager()
    dbfunctions: AccountingBehaviorManager = AccountingBehaviorManager()

    class Meta:
        permissions: list[tuple[str, str]] = []
        verbose_name: str = "Accounting behavior"
        verbose_name_plural: str = "Accounting behaviors"
        get_latest_by: str = "-created_at"
        ordering: list[str] = ["tag", "folio"]

    @property
    def pk(self: Self) -> int:
        return self.id

    @property
    def is_active(self: Self) -> bool:
        return self.deprecated_at is not None

    def __str__(self: Self) -> str:
        return '{} {}'.format(
            str(self.folio).zfill(2),
            self.label,
        )

    def save(self: Self, *args, **kwargs) -> str :
        self.name: str = self.name.strip().lower()
        super().save(*args, **kwargs)

    def get_absolute_url(self: Self) -> str:
        return reverse("account_behavior", kwargs={"pk": self.pk})
