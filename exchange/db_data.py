import sqlite3
import os.path

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

CURRENCES_CHOICES = [code for code in curr_in_nbp if code[0] not in list_of_currences_in_db]