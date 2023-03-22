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