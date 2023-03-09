from django import forms
from django.core.validators import MaxValueValidator
import sqlite3
import os.path
from .models import ExchangeRates, Invoices
from datetime import date, timedelta
from django.contrib import admin


def get_choices():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    db_path = os.path.join(BASE_DIR, "db.sqlite3")
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        curences_in_db = cursor.execute("Select distinct currency from exchange_exchangerates;")

    list_of_currences_in_db = [row[0] for row in curences_in_db]

    curr_in_nbp = [('AUD', 'AUD'),('BGN', 'BGN'),('BRL', 'BRL'),('CAD', 'CAD'),('CHF', 'CHF'),('CLP', 'CLP'),('CNY', 'CNY'),('CZK', 'CZK'),('DKK', 'DKK'),('EUR', 'EUR'),('GBP', 'GBP'),
    ('HKD', 'HKD'),('HUF', 'HUF'),('IDR', 'IDR'),('ILS', 'ILS'),('INR', 'INR'),('ISK', 'ISK'),('JPY', 'JPY'),('KRW', 'KRW'),('MXN', 'MXN'),('MYR', 'MYR'),('NOK', 'NOK'),('NZD', 'NZD'),
    ('PHP', 'PHP'),('RON', 'RON'),('SEK', 'SEK'),('SGD', 'SGD'),('THB', 'THB'),('TRY', 'TRY'),('UAH', 'UAH'),('USD', 'USD'),('XDR', 'XDR'),('ZAR', 'ZAR')
    ]

    return [code for code in curr_in_nbp if code[0] not in list_of_currences_in_db]




class DateInput(forms.DateInput):
    input_type = 'date'

class ExchangeRatesForms(forms.Form):
    currency = forms.ChoiceField(label= "Currency code", required=True, widget=forms.Select, choices=get_choices)
    start_date = forms.DateField(label = "Download rates from (example: 31.12.2022)"
                                ,error_messages = {'invalid':"Enter a valid date. Example: 31.12.2022"}
                                ,widget = DateInput()
                                ,validators=[MaxValueValidator(date.today() - timedelta(days=1))])

class InvoicesForm(forms.ModelForm):
    query = ExchangeRates.objects.order_by('currency').values_list('currency', flat=True).distinct()
    # query_choices = [('', '---')] + [(code, code) for code in query]
    # inv_currency = forms.ChoiceField(choices=query_choices, required=True, widget=forms.Select)
    inv_currency = forms.ModelChoiceField(queryset=query, required=True, widget=forms.Select, to_field_name="currency", empty_label='---')
    class Meta:
        model = Invoices
        fields = ['companyname','inv_currency','inv_date','inv_amount','rate_date','is_paid']
        widgets ={
            'inv_date': DateInput,
            'rate_date': DateInput
        }