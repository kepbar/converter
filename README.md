# Converter

This website allows you to save your invoices in foreign currencies and convert them into PLN at the current exchange rate on a given day from NBP.

# Requirements
- Python
- Django
- SQLite3

# How to run project localy
```bash
python manage.py runserver
```
Optionally you can also add server number to change default runserver port, ex. python manage.py runserver 8010

# How to use app

To add a new invoice, click **Invoices** on navbar, then click **Add** and fill in the boxes. If you cannot find a currency in the dropdown list, you can download it from NBP. To do so, go to the **Exchange Rates** tab, click **Add** and select the currency (the list includes all currencies available on NBP, apart from these already downloaded) and the date of the currency exchange rate.

To download new exchange rates, go to the **Exchange Rates** tab, click **List & Refresh** and select the blue **Refresh** button. Below you will find a list with all downloaded currencies. The rates shown are from the previous day.

You can view invoices in two ways:
1) **Table** (**Invoices** => **Table**)
2) **List** (**Invoices** => **List**)

To edit invoices in table view, click the **Edit** button.
To edit invoices in list view, first click **Details** to go to detail view, then select **Edit**.
Once you have approved the changes, the rate and currency exchange rate will be updated. Next to the **Edit** button you will find a **Delete** button that allows you delete an invoice. 

Under **HOME & SUMMARY** you will find a summary of your saved invoices. The table contains a list of unpaid invoices, statistics, i.e. the sum of the invoice values for the current month, the previous month, YTD and the average monthly total for full months. In addition, the column chart shows the sum of invoice values for the last 12 months.
