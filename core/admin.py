from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Wallet, Transaction


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra info', {'fields': ('role', 'class_name')}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('from_wallet', 'to_wallet', 'amount', 'created_at')
    list_filter = ('created_at',)
