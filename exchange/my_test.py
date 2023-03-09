import sqlite3
import os.path
from decimal import Decimal
from datetime import datetime, timedelta, date


if __name__ == '__main__':
   data =  datetime.now() - timedelta(days=365)
   
   print(data)
