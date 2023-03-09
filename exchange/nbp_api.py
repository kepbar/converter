import requests
import json
from datetime import date, timedelta, datetime
from terminaltables import AsciiTable

def get_rate(currency, date_start, date_end):
    delta = timedelta(days=365)
    rates = []
    if ((date_end-date_start).days) < 365:
        url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_start}/{date_end}/?format=json"
        try:
            response = requests.get(url)
        except Exception as e:
            print(f"Error occurred: {e}, on url: '{url}'")
        else:
            if response.status_code == 200:
                rates.extend(json.loads(response.text)['rates'])
                return rates   
    else:
        while date_start <= date_end:
            if date_start + delta <= date_end:
                url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_start}/{date_start + delta}/?format=json"
                try:
                    response = requests.get(url)
                    date_start += delta
                except Exception as e:
                    print(f"Error occurred: {e}, on url: '{url}'")
                else:
                    rates.extend(json.loads(response.text)['rates'])
            else:
                url = f"https://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_start}/{date_end}/?format=json"
                try:
                    response = requests.get(url)
                    date_start += delta # to jest po to żeby zakończyć while
                except Exception as e:
                    print(f"Error occurred: {e}, on url: '{url}'")
                else:
                    if response.status_code == 200:
                        rates.extend(json.loads(response.text)['rates'])
                        return rates
        


#testowanie
if __name__ == '__main__':
    i=1
    currency = "EUR"
    date_start = date.fromisoformat('2021-01-01')
    date_end = (datetime.today().date() - date(days=1))    
            
    rows = [
        ['currency', 'currency_date', 'mid_rate']
        ]
    for element in get_rate(currency, date_start, date_end):
        rows.append([
                    currency,
                    element['effectiveDate'],
                    element['mid']
                 ])
    table = AsciiTable(rows)
    print(table.table)
    #print(get_rate(currency, date_start, date_end))