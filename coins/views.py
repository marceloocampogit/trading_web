from django.shortcuts import render, redirect

# Create your views here.

def coin_details(request):
    return render(request, 'coins/coin-details.html')

def my_wallets(request):
    return render(request, 'coins/my-wallets.html')

def portfolio(request):
    return render(request, 'coins/portfolio.html')