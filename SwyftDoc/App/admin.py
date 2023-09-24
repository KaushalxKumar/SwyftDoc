from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from App.forms import *
from App.models import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = Person
    add_form = CreateUserForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Attributes',
            {
                'fields': (
                    'verified',
                    'token',
                    'public_key',
                    'private_key',
                )
            }
        )
    )

    readonly_fields = ('public_key', 'private_key',)


admin.site.register(Person, CustomUserAdmin)
