from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.coreapp.models.currency import Currency
from apps.coreapp.models.entity import Entity
from apps.coreapp.models.profile import Profile
from apps.coreapp.models.user import User

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Currency)
admin.site.register(Entity)
