from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from coins.models import Coin, Transactions
from coins.utils import get_five_days_data, get_recent_transactions

import json

@login_required
def index(request):
    #for coin in Coin.objects.all():
    #    print(coin.get_performance())
    context = {
        'graph_data': json.dumps(get_five_days_data()),
        'coins': Coin.objects.all(),
        'recent_transactions': get_recent_transactions()
    }
    return render(request, 'index.html', context=context)