from django.test import TestCase
from models import ExchangeRates
# Create your tests here.
from nbp_api import get_rate

#types = [(ExchangeRates.objects.order_by('currency').values('currency').distinct(),ExchangeRates.objects.order_by('currency').values('currency').distinct())]
    

print(ExchangeRates.objects.order_by('currency').values_list('currency').distinct())
