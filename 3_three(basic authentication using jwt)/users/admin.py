"""
Docstring for users.admin
"""
# core imports
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# local imports
from .models import Account

@admin.register(Account)
class Admin(UserAdmin):
    """
    here i am configuring admin panel for user
    """
    list_display = []
    list_filter = []
    search_fields = []
    ordering = []

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