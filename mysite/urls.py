from typing import Any

from django.contrib import admin
from django.urls import path

from apps.accounting.views import BalancePageView
from apps.coreapp.views import HomePageView

urlpatterns: list[Any] = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("overview", BalancePageView.as_view(), name="overview"),
]