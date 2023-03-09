from django.db import models
from django import forms
import sqlite3
import os.path
from decimal import Decimal
from datetime import timedelta

# Create your models here.
class DateInput(forms.DateInput):
    input_type = 'date'

class ExchangeRates(models.Model):
    currency = models.CharField(max_length=3)
    rate_date = models.DateField()
    mid_rate = models.DecimalField(max_digits=20, decimal_places=4)

    def __str__(self):
        return self.currency

class Invoices(models.Model):
    companyname = models.CharField(max_length=100, verbose_name=('Company name:'))
    inv_currency = models.CharField(max_length=3, verbose_name=('Invoice currency:'))
    #inv_currency = models.ForeignKey(ExchangeRates, on_delete=models.CASCADE,verbose_name=('Invoice currency:'))
    inv_date = models.DateField(verbose_name=('Invoice date:'))
    inv_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=('Invoice amount:'))
    rate_date = models.DateField(verbose_name=('Date of exchange rate:'))
    inv_amount_PLN = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(verbose_name=('Is paid:'))
    rate = models.DecimalField(max_digits=10, decimal_places=4)
    def get_rate(self):
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
        db_path = os.path.join(BASE_DIR, "db.sqlite3")
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"Select distinct mid_rate from exchange_exchangerates where rate_date = '{self.rate_date}' and currency = '{self.inv_currency}';")
            row = next(cursor, [None])[0]
            print(type(self.rate_date))
            while row == None:
                self.rate_date = self.rate_date - timedelta(days=1)
                cursor = db.cursor()
                cursor.execute(f"Select distinct mid_rate from exchange_exchangerates where rate_date = '{self.rate_date}' and currency = '{self.inv_currency}';")
                row = next(cursor, [None])[0]
                
        return Decimal(str(row))

    def save(self, *args, **kwargs):
        self.inv_amount_PLN = self.inv_amount * self.get_rate()
        self.rate = self.get_rate()
        super(Invoices, self).save(*args, **kwargs)

   

    def __str__(self):
        return f"""companyname: {self.companyname} \n, 
                    inv_currency: {self.inv_currency} \n,
                    inv_date: {self.inv_date} \n,
                    inv_amount: {self.inv_amount} \n,
                    rate_date: {self.rate_date} \n,
                    inv_amount_PLN: {self.inv_amount_PLN} \n,
                    is_paid: {self.is_paid} \n,
                    companyname: {self.companyname} \n"""