from django.urls import path
from . import views

#app_name = "exchange"
app_name = "exchange"

urlpatterns =[
    path('invoice_add/', views.InvoicesCreateView.as_view(), name = 'invoice_add'),
    path('invoices_list/', views.InvoicesListView.as_view(), name ='invoices_list'),
    path('invoices_table/', views.InvoicesTableListView.as_view(), name ='invoices_table'),
    path('invoice_detail/<int:pk>', views.InvoicesDetailView.as_view(), name = 'invoice_detail'),
    path('invoice_update/<int:pk>', views.InvoicesUpdateView.as_view(), name = 'invoice_update'),
    path('invoice_delete/<int:pk>', views.InvoicesDeleteView.as_view()),
    path('add_rates/', views.add_rates, name = 'add_rates'),
    path('list_rates/', views.RatesListView.as_view(), name = 'list_rates'),
    path('home/', views.HomeView.as_view(), name = 'home'),
    path('welcome/', views.welcome, name = 'welcome'),
]