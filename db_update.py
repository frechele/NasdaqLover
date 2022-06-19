import psycopg2 as pg2
import yfinance
import pandas_datareader as pdr
import pandas as pd
import logging

from core.config import CONFIG


class DBUpdater:
    def __init__(self):
        self.config = CONFIG['db']
        self.conn = pg2.connect(host=self.config['host'], port=self.config['port'], database='nasdaq',
                                user=self.config['user'], password=self.config['passwd'])

        self.table_tickers = {
            'nasdaq': '^IXIC',
            'vix': '^VIX',
            'nasdaqFut': 'NQ=F',
            'krw': 'KRW=X'
        }
        self._init_db()

    def __del__(self):
        self.conn.close()

    def update_tables(self):
        for table_name, ticker in self.table_tickers.items():
            self.update_table(table_name, ticker)

    def update_table(self, table_name: str, ticker: str):
        with self.conn.cursor() as curs:
            sql = f'''
            SELECT MAX(date) FROM {table_name};
            '''
            curs.execute(sql)
            start_date = curs.fetchone()[0]

            if start_date is None:
                start_date = '1900-01-01'

            logging.info(f'update table {table_name} after {start_date}')
            df = DBUpdater.get_data_from_yahoo(ticker, start_date)
            sql = f'INSERT INTO {table_name} VALUES '
            for i, r in enumerate(df.itertuples()):
                if i > 0:
                    sql += ', '
                sql += f"( '{r.Date}', '{r.Open}', '{r.High}', '{r.Low}', '{r.Close}' )"
            sql += ' ON CONFLICT (date) DO NOTHING'

            curs.execute(sql)
            self.conn.commit()

    @staticmethod
    def get_data_from_yahoo(ticker: str, start: str) -> pd.DataFrame:
        df = pdr.get_data_yahoo(ticker, start=start)[
            ['High', 'Low', 'Open', 'Close']]
        df = df.reset_index(level='Date')
        return df

    def _init_db(self):
        with self.conn.cursor() as curs:
            for table_name in self.table_tickers:
                sql = f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                    date DATE,
                    open FLOAT,
                    high FLOAT,
                    low FLOAT,
                    close FLOAT,
                    PRIMARY KEY (date)
                );
                '''
                curs.execute(sql)


if __name__ == '__main__':
    db = DBUpdater()

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    db.update_tables()
