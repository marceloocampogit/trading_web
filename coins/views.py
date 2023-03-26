from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import timedelta, datetime

import random
import json

from coins.utils import generate_transactions
from coins.models import Coin, Transactions, Card
from coins.forms import CardForm

# Create your views here.

@login_required
def coin_details(request, id):
    if request.method == 'GET':
        
        context = {
            'coin': Coin.objects.get(pk=id),
            'graph_data': json.dumps(Coin.objects.get(pk=id).get_last_ten_days_data()),
            #'graph_data': Coin.objects.get(pk=id).get_last_ten_days_data(),

        }

        print(context['graph_data'])
        return render(request, 'coins/coin-details.html', context = context)


@login_required
def my_wallets(request):
    if request.method == 'GET':
        context = {
            'cards': Card.objects.filter(user=request.user)
        }
        return render(request, 'coins/my-wallets.html', context=context)
    
    elif request.method == 'POST':

        data = request.POST.copy()
        data['valid_date'] = datetime.strptime(request.POST['valid_date'], '%m/%y').date()

        form = CardForm(data)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.balance = random.randint(5000, 30000)
            card.save()
            return redirect('my_wallets')
        else:
            context = {
                'cards': Card.objects.filter(user=request.user),
                'errors': form.errors,
            }
            return render(request, 'coins/my-wallets.html', context=context)

@login_required
def portfolio(request):
    return render(request, 'coins/portfolio.html')

def generate_data(request):
    generate_transactions()
    return HttpResponse('Data generated')