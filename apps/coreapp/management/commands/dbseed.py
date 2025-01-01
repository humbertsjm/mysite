# pylint: skip-file
import json
from typing import Any

from django.core.management.base import BaseCommand

from apps.accounting.models.account import Account
from apps.accounting.models.accounting_behavior import AccountingBehavior
from apps.accounting.models.exchange_ratio import ExchangeRatio
from apps.coreapp.enums import AccountingCategoryTag, CurrencyTag, EntityTag
from apps.coreapp.models.currency import Currency
from apps.coreapp.models.entity import Entity
from apps.coreapp.models.json_models import SeedJSON
from apps.coreapp.models.profile import Profile
from apps.coreapp.models.user import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> None:
        JSON_PATH = 'seed.json'
        # from apps.coreapp.management.commands._private import reset_db
        # reset_db()

        seed_json: Any = None
        with open(JSON_PATH, 'r') as json_file:
            seed_json = json.load(json_file)

        seed: SeedJSON = SeedJSON.from_dict(seed_json)

        for i, p in enumerate(seed.profiles):
            user: User = User.objects.get(username=p.from_username)
            Profile.dbfunctions.new_profile(
                p.name,
                p.label,
                user,
                _display_order=i + 1,
            )

        for i, c in enumerate(seed.currencies):
            tag: CurrencyTag = CurrencyTag[c.currency_tag_enum]
            Currency.dbfunctions.new_currency(
                c.name,
                c.label,
                tag.value,
                _display_order=i + 1,
            )

        for i, e in enumerate(seed.entities):
            tag: EntityTag = EntityTag[e.entity_tag_enum]
            Entity.dbfunctions.new_entity(
                e.name,
                e.label,
                tag,
                _display_order=i + 1,
            )

        for i, b in enumerate(seed.accounting_behaviors):
            tag: AccountingCategoryTag = AccountingCategoryTag[
                b.accounting_category_tag_enum
            ]
            AccountingBehavior.dbfunctions.new_accounting_behavior(
                tag,
                i + 1,
                b.name,
                b.label,
            )

        for i, a in enumerate(seed.accounts):
            profile: Profile = Profile.objects.get(name=a.owner)
            entity: Entity = Entity.objects.get(name=a.entity)
            behavior: AccountingBehavior = AccountingBehavior.objects.get(
                name=a.behavior
            )
            currency: Currency = Currency.objects.get(name=a.currency)
            Account.dbfunctions.new_account(
                a.label,
                profile,
                entity,
                behavior,
                currency,
            )

        for i, e in enumerate(seed.exchange_ratios):
            from_c: Currency = Currency.objects.get(name=e.from_currency)
            tp_c: Currency = Currency.objects.get(name=e.to_currency)
            ExchangeRatio.dbfunctions.new_ratio(
                from_c,
                tp_c,
                e.ratio,
            )
