from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from .models import ExchangeRates, Invoices
from .nbp_api import get_rate
from .forms import ExchangeRatesForms, InvoicesForm
from datetime import date, timedelta, datetime
import sqlite3
import os.path
import json


class HomeView(ListView):
    model = Invoices
    
    template_name = 'exchange/home.html'
    context_object_name = "unpaid_invoices"

    def get_queryset(self):
        return Invoices.objects.order_by('-inv_date').filter(is_paid=0)

    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context['curr_month']=Invoices.objects.filter(inv_date__year=(datetime.now().year), inv_date__month=(datetime.now().month)).aggregate(Sum('inv_amount_PLN'))
        context['prev_month']=Invoices.objects.filter(inv_date__year=(datetime.now().year), inv_date__month=(datetime.now().month-1)).aggregate(Sum('inv_amount_PLN'))
        context['YTD']=Invoices.objects.filter(inv_date__year=(datetime.now().year)).aggregate(ytd_sum = Sum('inv_amount_PLN'))
        context['YTD_full_months']=Invoices.objects.filter(inv_date__year=(datetime.now().year), inv_date__month__lt=(datetime.now().month)).aggregate(
            ytd_avg_month = Sum('inv_amount_PLN')/(datetime.now().month-1))
        context['sales_by_month'] = Invoices.objects.values('inv_date__month').annotate(inv_pln_sum=Sum('inv_amount_PLN'))
        
        bar_data = Invoices.objects.filter(inv_date__gt=(datetime.now() - timedelta(days=365))).values('inv_date__month').annotate(inv_pln_sum=Sum('inv_amount_PLN')).order_by('-inv_date__month')
        labels = []
        data = []
        for entry in bar_data:
            labels.append(entry['inv_date__month'])
            #labels.append(date(1900, (entry['inv_date__month']), 1).strftime('%B'))
            data.append(int(entry['inv_pln_sum']))
               
        context['monthly_sales_labels'] = labels
        context['monthly_sales_values'] = data

        context['data'] = json.dumps({
                                        'labels': labels,
                                        'data': data,
                                    })
        # chart_usdpln_data = ExchangeRates.objects.filter(currency='USD')
        # labels = []
        # data = []
        # for entry in chart_usdpln_data:
        #     labels.append(entry['rate_date'])
        #     data.append(int(entry['mid_rate']))
               
        # context['chart_usdpln_labels'] = labels
        # context['chart_usdpln_values'] = data


        return context


class InvoicesCreateView(SuccessMessageMixin, CreateView):
    form_class = InvoicesForm
    success_url = reverse_lazy('exchange:invoice_add') 
    template_name = 'exchange/invoices.html'
    success_message = 'Invoice added corectly'

class InvoicesListView(ListView):
    model = Invoices
    template_name = 'exchange/invoices_list.html'
    queryset = Invoices.objects.order_by('-inv_date').all()
    context_object_name = "invoices_list"

class InvoicesTableListView(ListView):
    model = Invoices
    template_name = 'exchange/invoices_table.html'
    queryset = Invoices.objects.order_by('-inv_date').all()
    context_object_name = "invoices_table"

class InvoicesDetailView(DetailView):
    model = Invoices
    template_name = 'exchange/invoices_detail.html'

class InvoicesUpdateView(UpdateView):
    model = Invoices
    form_class = InvoicesForm    
    template_name = 'exchange/invoices.html'
    success_url = reverse_lazy('exchange:invoices_table')

class InvoicesDeleteView(DeleteView):
    model = Invoices
    success_url = reverse_lazy('exchange:invoices_table')
    #template_name = 'exchange/invoice_confirm_delete.html' 

def add_rates(request):
    #POST REQUEST --> FORM CONTENTS --> CONGRATS & Download from NBP
    if request.method == 'POST':
        form = ExchangeRatesForms(request.POST)
        if form.is_valid(): #pobranie kursów z NBP
            rates_list = get_rate(
                    form.cleaned_data['currency'],
                    form.cleaned_data['start_date'],
                    (date.today() - timedelta(days=1))
                    )
            connection = sqlite3.connect('db.sqlite3').cursor()
            for rate in rates_list: # przekazanie pobranych danych jeden po drugim do modelu i sprawdzenie czy już nie występują dane rekordy w bazie
                connection.execute(f"""select rowid 
                                    from exchange_exchangerates
                                    where currency='{form.cleaned_data['currency']}' 
                                    and rate_date = '{rate['effectiveDate']}';""")
                db_result=connection.fetchall()

                if len(db_result)==0:
                    rate_value = ExchangeRates(
                        currency = form.cleaned_data['currency'],
                        rate_date = rate['effectiveDate'],
                        mid_rate = rate['mid']
                    )
                    rate_value.save()
                else:
                    next
            connection.close()
            
            messages.success(request, 'Echange rates for new currency added')
            return render(request, 'exchange/add_rates.html', context={'form':form}) #wracamy do głównej strony
    else: 
        form = ExchangeRatesForms()

    return render(request, 'exchange/add_rates.html', context={'form':form})

class RatesListView(ListView):
    model = ExchangeRates
    queryset = ExchangeRates.objects.order_by('currency').values('currency').distinct()
    context_object_name = "rates_list"

    def get(self, request, *args, **kwargs):
        return super(RatesListView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #refresh rates
        if request.method == 'POST' and 'refresh_button' in request.POST:
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
            db_path = os.path.join(BASE_DIR, "db.sqlite3")
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                curences_in_db = cursor.execute("select currency, max(rate_date) from exchange_exchangerates group by currency;")

            tuples_curr_dates = [(row[0],date.fromisoformat(row[1])) for row in curences_in_db]

            
            for tuple in tuples_curr_dates:
                rates_list = get_rate(
                    tuple[0],
                    tuple[1],
                    (date.today() - timedelta(days=1)))
                connection = sqlite3.connect('db.sqlite3').cursor()
                for rate in rates_list: # przekazanie pobranych danych jeden po drugim do modelu i sprawdzenie czy już nie występują dane rekordy w bazie
                    connection.execute(f"""select rowid 
                                        from exchange_exchangerates
                                        where currency='{tuple[0]}' 
                                        and rate_date = '{rate['effectiveDate']}';""")
                    db_result=connection.fetchall()

                    if len(db_result)==0:
                        rate_value = ExchangeRates(
                            currency = tuple[0],
                            rate_date = rate['effectiveDate'],
                            mid_rate = rate['mid']
                        )
                        rate_value.save()
                    else:
                        next
                connection.close()
            
            messages.success(self.request, 'Rates refreshed')
            return super(RatesListView, self).get(request, *args, **kwargs)
        else:
            #nie ma przycisku, nie ma odświeżania
            return super(RatesListView, self).get(request, *args, **kwargs)

def welcome(request):
    return render(request, 'exchange/welcome.html')