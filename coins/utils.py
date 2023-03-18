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