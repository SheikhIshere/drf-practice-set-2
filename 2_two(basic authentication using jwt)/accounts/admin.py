"""
Docstring for accounts.admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdminUser
from django.utils.translation import gettext_lazy as _
from .models import Accounts


@admin.register(Accounts)
class UserAdmin(BaseAdminUser):
    """
    Docstring for UserAdmin
    """

    # fields
    list_display = (
        'email', 'name', 'is_staff', 'is_active', 'date_joined'
    )
    list_filter = (
        'is_active', 'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'name')
    ordering = ('id', 'email')

        # Fieldsets define the layout of the admin “edit” page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal info'), {'fields': ('name')}),
        (_('Personal info'), {'fields': ('name',)}),

        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to use when creating a new user via admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
