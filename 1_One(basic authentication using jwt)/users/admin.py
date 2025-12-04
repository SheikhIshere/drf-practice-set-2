from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no username field required."""

    # Fields to display in the admin list view
    list_display = ('email', 'username', 'name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)

    # Fieldsets define the layout of the admin “edit” page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'username')}),
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

admin.site.register(User, UserAdmin)
