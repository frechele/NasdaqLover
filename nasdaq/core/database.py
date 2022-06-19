import psycopg2 as pg2
import pandas as pd
from datetime import datetime, timedelta
import re

from nasdaq.core.config import CONFIG


class Database:
    def __init__(self):
        self.config = CONFIG['db']
        self.conn = pg2.connect(host=self.config['host'], port=self.config['port'], database='nasdaq',
                                user=self.config['user'], password=self.config['passwd'])

    @property
    def table_names(self):
        return ['nasdaq', 'nasdaqFut', 'vix', 'krw', 'wti']

    def get_daily_price(self, table, start_date=None, end_date=None):
        start_date, end_date = self._date_convert(start_date, end_date)
        sql = f"SELECT * FROM {table} WHERE date >= '{start_date}' AND date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df

    def __del__(self):
        self.conn.close()

    @staticmethod
    def _date_convert(start_date, end_date):
        if start_date is None:
            start_date = datetime.today() - timedelta(days=365)
            start_date = start_date.strftime('%Y-%m-%d')
        else:
            start_lst = re.split('\D+', start_date)
            if len(start_lst[0]) == 0:
                start_lst = start_lst[1:]
            
            start_year, start_month, start_day = map(int, start_lst)
            start_date = f'{start_year:04d}-{start_month:02d}-{start_day:02d}'

        if end_date is None:
            end_date = datetime.today()
            end_date = end_date.strftime('%Y-%m-%d')
        else:
            end_lst = re.split('\D+', end_date)
            if len(end_lst[0]) == 0:
                end_lst = end_lst[1:]
            
            end_year, end_month, end_day = map(int, end_lst)
            end_date = f'{end_year:04d}-{end_month:02d}-{end_day:02d}'

        return start_date, end_date
