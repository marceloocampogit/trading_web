from datetime import timedelta

from django.utils import timezone

import random

from coins.models import Transactions, Coin

def generate_price():
    return random.randint(10000, 30000) * random.random()

def generate_amount():
    return random.randint(1, 200) * random.random()

def generate_transaction_type():
    return random.choice(['buy', 'sell'])

def generate_transactions():

    transactions_to_create = []

    for coin in Coin.objects.all(): #Each coin
        today = timezone.now()

        for i in range(1, 31): #Each day

            for j in range(1, 31): #Each transaction
                new_transaction = Transactions(
                    coin = coin,
                    price = generate_price(),
                    amount = generate_amount(),
                    date = today,
                    transaction_type = generate_transaction_type()
                )
                transactions_to_create.append(new_transaction)

            today -= timedelta(days=1)
    Transactions.objects.bulk_create(transactions_to_create)

def get_five_days_data():

    context = {
        'data': []
    }
    #Obtengo fechas para mi array
    dates_array = [Transactions.get_last_day()]

    for i in range(1, 5):
        #Voy haciendo mi insert de fechas 1 a 1
        dates_array.append( (dates_array[0] - timedelta(days=1)).strftime('%d/%m') )

    #Formateamos la primer fecha
    dates_array[0] = dates_array[0].strftime('%d/%m')

    #Revertimos el array para que quede de la forma que necesito
    dates_array.reverse()

    #Agregamos el array de fechas al contexto
    context['dates'] = dates_array

    count = 0
    for coin in Coin.objects.all():
        context['data'].append(
            {
            'name': coin.name,
            'data': coin.get_last_five_days_data()
            }
        )

    return context

def get_recent_transactions():
    since_day = Transactions.get_last_day() - timedelta(days=2)
    return random.choices(Transactions.objects.filter(date__gte=since_day), k=6)