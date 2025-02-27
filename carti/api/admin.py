from django.contrib import admin
from .models import BankAccount

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'owner', 'balance', 'currency')
    search_fields = ('account_number', 'owner')

# Ou en simple :
# admin.site.register(BankAccount)
