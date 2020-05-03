from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Include Django's transalation engine
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    # see https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
    ordering = ['id']
    list_display = ['username', 'email']

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal Information'), {
            'fields': ('email',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        (_('Important Dates'), {
            'fields': ('last_login',)
        }),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a users.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.register(models.User, UserAdmin)
