from pandas_datareader import data as pdr
import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Tuple, List
import numpy as np


def _convert_none_to_str(start_date: str, end_date: str) -> Tuple[str, str]:
    if start_date is None:
        start_date = '1900-01-01'
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    return start_date, end_date


def get_nasdaq_index(start_date: str=None, end_date: str=None) -> pd.DataFrame:
    start_date, end_date = _convert_none_to_str(start_date, end_date)

    return pdr.get_data_yahoo("^IXIC", start=start_date, end=end_date)


def get_nasdaq_future(start_date: str=None, end_date: str=None) -> pd.DataFrame:
    start_date, end_date = _convert_none_to_str(start_date, end_date)

    return pdr.get_data_yahoo("NQ=F", start=start_date, end=end_date)


def get_vix_index(start_date: str=None, end_date: str=None) -> pd.DataFrame:
    start_date, end_date = _convert_none_to_str(start_date, end_date)

    return pdr.get_data_yahoo("^VIX", start=start_date, end=end_date)


def get_krw_index(start_date: str=None, end_date: str=None) -> pd.DataFrame:
    start_date, end_date = _convert_none_to_str(start_date, end_date)

    return pdr.get_data_yahoo("KRW=X", start=start_date, end=end_date)


def calc_returns(prices: np.ndarray) -> np.ndarray:
    returns = np.zeros(len(prices) - 1)

    for i in range(len(returns)):
        returns[i] = (prices[i + 1] - prices[i]) / prices[i]

    return returns


def split_data(df: pd.DataFrame, window_size: int) -> List[pd.DataFrame]:
    result = []

    for i in range(len(df) - window_size + 1):
        result.append(df[i:i + window_size])

    return result


if __name__ == '__main__':
    nasdaq = get_nasdaq_index()
    nasfut = get_nasdaq_future()
    vix = get_vix_index()
    krw = get_krw_index()

    nasdaq.to_csv('nasdaq.csv')
    nasfut.to_csv('nasfut.csv')
    vix.to_csv('vix.csv')
    krw.to_csv('krw.csv')
