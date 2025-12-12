"""
Docstring for account.admin
"""

# core imports
from django.contrib.admin import ModelAdmin
from django.contrib import admin


# local imports
from .models import Account


@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined'
    )

    # search_fields = ('email')
