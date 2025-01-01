# pylint: disable=C0301
from typing import Literal

from django.db import models
from django.utils.translation import gettext_lazy as _

# """
# class EnumExample(models.IntegerChoices):
#     ITEM = "1", _("Example item")
#     # value: 1
#     # name: ITEM
#     # label: Example item
#     # choice: (1, "Example item")
# """
DEFAULT_DISPLAY_ORDER = 99
DEFAULT_FOLIO = 99


class CurrencyTag(models.IntegerChoices):
    MONEY: tuple[Literal[0], str] = 0, _("Money (FIAT currency)")
    POINT: tuple[Literal[1], str] = 1, _("Points (Rewards/Loyalty/Exchange digital points)")
    INVESTMENT_UNIT: tuple[Literal[2], str] = 2, _("Investment unit (ETF, stock, bonds, treasure titles, etc)")
    CRYPTO: tuple[Literal[3], str] = 3, _("Crypto currency (NFT excluded)")
    TOKEN: tuple[Literal[4], str] = 4, _("Token (NFT or any other unique item)")
    OTHER: tuple[Literal[99], str] = 99, _("Other")

    @classmethod
    def get_label(cls, _tag: int) -> str:
        return cls.labels[
            cls.values.index(_tag)
        ]


class AccountingCategoryTag(models.IntegerChoices):
    ASSET: tuple[Literal[1], str] = 1, _("Asset")
    LIABILITY: tuple[Literal[2], str] = 2, _("Liability")
    EQUITY: tuple[Literal[3], str] = 3, _("Equity")


class EntityTag(models.IntegerChoices):
    NOTHING: tuple[Literal[0], str] = 0, _("Nothing")

    # Misc 1 - 19
    STORAGE: tuple[Literal[1], str] = 1, _("Any storage/container for valuables")

    # Relatives 20 - 39
    ME: tuple[Literal[20], str] = 20, _("Me (myself)")

    # Physical person 40-59
    PERSON: tuple[Literal[40], str] = 40, _("Person")
    CUSTOMER: tuple[Literal[41], str] = 41, _("Customer")
    SALESPERSON: tuple[Literal[42], str] = 42, _("Sales person")

    # Virtual/moral person 60-69
    BANK: tuple[Literal[60], str] = 60, _("Bank")
    FINTECH: tuple[Literal[61], str] = 61, _("Fintech")
    COMPANY: tuple[Literal[62], str] = 62, _("Financial service")
    BROKER: tuple[Literal[63], str] = 63, _("Exchange broker")

    # Properties 70-79
    HOUSE: tuple[Literal[70], str] = 70, _("House")
    TERRAIN: tuple[Literal[71], str] = 71, _("Terrain")
    VEHICLE: tuple[Literal[72], str] = 72, _("Vehicle")

    # Misc 90-99
    OTHER: tuple[Literal[99], str] = 99, _("Other")

    @classmethod
    def get_label(cls, _tag) -> str:
        return cls.labels[
            cls.values.index(_tag)
        ]
