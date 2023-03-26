from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Sum
from datetime import timedelta

class Card(models.Model):

    CHOICES = (
        ('purple', 'purple'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('orange', 'orange'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'cards')
    card_name = models.CharField(max_length=40)
    card_holder = models.CharField(max_length=60)
    card_number = models.IntegerField(validators=[
                                                MinValueValidator(1000000000000000),
                                                MaxValueValidator(9999999999999999)
                                                ])
    bank_name = models.CharField(max_length=80)
    valid_date = models.DateField()
    color = models.CharField(max_length= 6, choices= CHOICES, default= 'purple')

    def __str__(self) -> str:
        return self.card_name
    

class Coin(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    description = models.TextField()
    image = models.ImageField(upload_to='coins')

    def __str__(self) -> str:
        return self.name
    
    #Devuelve el ultimo dia que se hizo una transaccion
    def get_last_day(self):
        return self.transactions.all().order_by('-date').first().date
    
    #Devuelve el promedio de transacciones por dia
    def get_price_by_date(self, date):
        return self.transactions.filter(date__date = date).aggregate(average = Avg('price'))['average']
    
    #Devuelve un array con los promedios de las ultimas 5 transacciones
    def get_last_five_days_data(self):
        data = []
        last_day = self.get_last_day()
        for i in range(1, 6):
            data.append(round(self.get_price_by_date(last_day), 2))
            last_day -= timedelta(days=1)
        return data

    def get_last_day_price(self):
        last_day = self.get_last_day()
        return round(self.get_price_by_date(last_day), 2)
    
    def get_performance_of_week(self, end_date):
        week_price = 0
        for i in range(0, 7):
            week_price += self.get_price_by_date(end_date)
            end_date -= timedelta(days=1)
        week_price /= 7
        return week_price, end_date
    
    #Devuelve el porcentaje de ganancia o perdida de la ultima semana
    def get_performance(self):
        last_day = self.get_last_day()
        actual_week_price, last_day = self.get_performance_of_week(last_day)
        last_week_price, last_day = self.get_performance_of_week(last_day)
        return round(((actual_week_price - last_week_price) / (last_week_price)) * 100, 2)
    
    def get_performance_24(self):
        last_day = self.get_last_day()
        actual_price = self.get_price_by_date(last_day)
        last_day -= timedelta(days=1)
        previous_price = self.get_price_by_date(last_day)
        return round(((actual_price - previous_price) / (previous_price)) * 100, 2)
    
    #Devuelve un array con las ultimas 7 transacciones
    def get_lasts_transactions(self):
        if self.transactions.count() == 0:
            return []
        return self.transactions.order_by('-date')[:7]
    
    def get_last_ten_days_data(self):
        data = []
        day = {}
        last_day = self.get_last_day()
        for i in range(1, 11):
            
            day = {
                'date': last_day.strftime('%d/%m'),
                'price': round(self.get_price_by_date(last_day), 2)
            }
            data.append(day)
            last_day -= timedelta(days=1)
        return data
    
    def get_trading_volume(self):
        date = self.get_last_day()
        return round(self.transactions.filter(date__date = date).aggregate(trading_volume = Sum('amount'))['trading_volume'],2 )
    
    def get_trading_volume_coin(self):
        date = self.get_last_day()
        last_day_price = self.get_last_day_price()
        return round(self.transactions.filter(date__date = date).aggregate(volume = (Sum('amount') * last_day_price))['volume'], 2)

class Transactions(models.Model):

    CHOICE = (
        ('buy', 'buy'),
        ('sell', 'sell'),
    )

    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name= 'transactions')
    price = models.FloatField()
    amount = models.FloatField()
    date = models.DateTimeField()
    transaction_type = models.CharField(max_length=10, choices= CHOICE)


    def __str__(self) -> str:
        return self.coin.name + ' ' + self.transaction_type + ' ' + str(self.date)
    
    @classmethod
    def get_last_day(cls):
        return cls.objects.all().order_by('-date').first().date.date()
    
    def get_total_price(self):
        return round(self.price * self.amount, 2)