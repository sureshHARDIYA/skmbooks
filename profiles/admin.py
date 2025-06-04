from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

from django.utils.translation import gettext_lazy as _


class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active", "user_type"]
    ordering = ["email"]
    search_fields = ["email", "first_name", "last_name"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", 'user_type', 'gender'),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", 'user_type', 'gender')}),
        (
            _("Permissions"),
            {
                "fields": ("groups", "user_permissions", 'is_staff', 'is_superuser', 'is_active'),

            },
        ),
    )

    def get_model_perms(self, request):
        # This makes sure it's visible under "Authentication and Authorization"
        return super().get_model_perms(request)

admin.site.register(User, UserAdmin)
