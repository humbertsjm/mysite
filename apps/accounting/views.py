from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from apps.accounting.models.account import Account
from apps.accounting.models.accounting_behavior import AccountingBehavior
from apps.coreapp._views import ProfileDataMixin
from apps.coreapp.enums import AccountingCategoryTag


class BalancePageView(LoginRequiredMixin, ProfileDataMixin, TemplateView):
    template_name = "balance.html"

    def get_context_data(self, **kwargs):
        context: Any = super().get_context_data(**kwargs)

        context['assets'] = [
            {
                'label': beh.label,
                'items': [
                    {
                        'label': acc.label,
                        'qty': acc.quantity,
                        'currency': acc.currency.label
                    }
                    for acc in Account.dbfunctions.get_by_behavior(beh)
                ],
                'section_total': 0
            }
            for beh in AccountingBehavior.dbfunctions.get_by_tag(
                AccountingCategoryTag.ASSET
            )
        ]

        context['liabilities'] = [
            {
                'label': beh.label,
                'items': [
                    {
                        'label': acc.label,
                        'qty': acc.quantity,
                        'currency': acc.currency.label
                    }
                    for acc in Account.dbfunctions.get_by_behavior(beh)
                ],
                'section_total': 0
            }
            for beh in AccountingBehavior.dbfunctions.get_by_tag(
                AccountingCategoryTag.LIABILITY
            )
        ]

        context['equities'] = [
            {
                'label': beh.label,
                'items': [
                    {
                        'label': acc.label,
                        'qty': acc.quantity,
                        'currency': acc.currency.label
                    }
                    for acc in Account.dbfunctions.get_by_behavior(beh)
                ],
                'section_total': 0
            }
            for beh in AccountingBehavior.dbfunctions.get_by_tag(
                AccountingCategoryTag.EQUITY
            )
        ]

        return context
