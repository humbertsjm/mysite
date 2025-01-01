from dataclasses import dataclass
from typing import Any, Self


@dataclass
class SeedProfile:
    name: str
    label: str
    from_username: str

@dataclass
class SeedCurrency:
    name: str
    label: str
    currency_tag_enum: str

@dataclass
class SeedEntity:
    name: str
    label: str
    entity_tag_enum: str

@dataclass
class SeedAccountingBehavior:
    name: str
    label: str
    accounting_category_tag_enum: str

@dataclass
class SeedAccount:
    label: str
    owner: str
    entity: str
    behavior: str
    currency: str
    quantity: float = 0

@dataclass
class SeedExchangeRatio:
    from_currency: str
    to_currency: str
    ratio: float

@dataclass
class SeedJSON:
    profiles: list[SeedProfile]
    currencies: list[SeedCurrency]
    entities: list[SeedEntity]
    accounting_behaviors: list[SeedAccountingBehavior]
    accounts: list[SeedAccount]
    exchange_ratios: list[SeedExchangeRatio]

    def to_dict(self) -> dict[str, Any]:
        return {
            'profiles': [
                x.__dict__
                for x in self.profiles
            ],
            'currencies': [
                x.__dict__
                for x in self.currencies
            ],
            'entities': [
                x.__dict__
                for x in self.entities
            ],
            'accounting_behaviors': [
                x.__dict__
                for x in self.accounting_behaviors
            ],
            'accounts': [
                x.__dict__
                for x in self.accounts
            ],
            'exchange_ratios': [
                x.__dict__
                for x in self.exchange_ratios
            ],
        }

    @classmethod
    def from_dict(cls: Self, json_data: dict[str, Any]) -> Self:
        return cls(
            [
                SeedProfile(**x)
                for x in json_data.get('profiles')
            ],
            [
                SeedCurrency(**x)
                for x in json_data.get('currencies')
            ],
            [
                SeedEntity(**x)
                for x in json_data.get('entities')
            ],
            [
                SeedAccountingBehavior(**x)
                for x in json_data.get('accounting_behaviors')
            ],
            [
                SeedAccount(**x)
                for x in json_data.get('accounts')
            ],
            [
                SeedExchangeRatio(**x)
                for x in json_data.get('exchange_ratios')
            ],
        )
