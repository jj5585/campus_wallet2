from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Wallet, Transaction


# Admin branding
admin.site.site_header = "Campus Wallet Administration"
admin.site.site_title = "Campus Wallet Admin"
admin.site.index_title = "Dashboard"


class WalletInline(admin.StackedInline):
    """
    Show each user's wallet directly on the User change page.
    Assumes one wallet per user.
    """
    model = Wallet
    can_delete = False
    extra = 0
    max_num = 1


class TransactionFromInline(admin.TabularInline):
    """
    Show transactions where this wallet is the sender (from_wallet)
    on the Wallet page.
    """
    model = Transaction
    fk_name = "from_wallet"
    extra = 0
    readonly_fields = ("created_at",)


@admin.action(description="Reset selected wallet balances to 0")
def reset_balance(modeladmin, request, queryset):
    queryset.update(balance=0)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # List view of users
    list_display = ("id", "username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("email",)

    # Link wallet inline
    inlines = [WalletInline]

    # Edit form layout
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "role", "class_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Add user form (gives password1 & password2)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "class_name", "is_staff", "is_active"),
        }),
    )


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "balance")
    search_fields = ("user__username", "user__email")
    ordering = ("id",)
    actions = [reset_balance]
    inlines = [TransactionFromInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "from_wallet", "to_wallet", "amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("from_wallet__user__username", "to_wallet__user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
