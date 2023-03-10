from django.contrib import admin

from coins.models import Card

# Register your models here.
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'card_holder', 'card_number', 'bank_name', 'valid_date', 'color')