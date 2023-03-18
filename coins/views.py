from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import timedelta

from coins.utils import generate_transactions
from coins.models import Coin, Transactions

# Create your views here.

@login_required
def coin_details(request):
    return render(request, 'coins/coin-details.html')

@login_required
def my_wallets(request):
    return render(request, 'coins/my-wallets.html')

@login_required
def portfolio(request):
    return render(request, 'coins/portfolio.html')

def generate_data(request):
    generate_transactions()
    return HttpResponse('Data generated')

def get_five_days_data(request):
    context = {
        'data': []
    }
    #Obtengo fechas para mi array
    dates_array = [Transactions.get_last_day()]

    for i in range(1, 5):
        #Voy haciendo mi insert de fechas 1 a 1
        dates_array.append(dates_array[0] - timedelta(days=1))

        count = 0
        for coin in Coin.objects.all():
            context['data'].append(
                {
                'name': coin.name,
                'data': coin.get_last_five_days_data()
                }
            )
        print(context)
    return HttpResponse('Data')