from django.urls import path

from .views import coin_details, my_wallets, portfolio

urlpatterns = [
    path('coin-details/', coin_details, name='coin_details'),
    path('my-wallets/', my_wallets, name='my_wallets'),
    path('portfolio/', portfolio, name='portfolio'),
]