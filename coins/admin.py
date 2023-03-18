from django.contrib import admin

from coins.models import Card, Coin, Transactions

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'card_holder', 'card_number', 'bank_name', 'valid_date', 'color')

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'description', 'image')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('coin', 'price', 'amount', 'date', 'transaction_type')