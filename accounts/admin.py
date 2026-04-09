from django.contrib import admin
from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance')
    search_fields = ('user__username', 'account_number')
    readonly_fields = ('account_number',)  # номер счёта не редактируем вручную
