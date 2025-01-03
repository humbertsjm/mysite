from django.contrib import admin

from apps.accounting.models.account import Account
from apps.accounting.models.accounting_behavior import AccountingBehavior
from apps.accounting.models.exchange_ratio import ExchangeRatio
from apps.accounting.models.account_snapshot import AccountSnapshot

admin.site.register(Account)
admin.site.register(ExchangeRatio)
admin.site.register(AccountingBehavior)
admin.site.register(AccountSnapshot)
