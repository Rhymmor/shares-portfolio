from typing import Any, Iterable, List, OrderedDict
import numpy as np
from numpy.typing import NDArray
from src.domain.stock_returns import StockReturns

def get_monthly_from_year(data: StockReturns, from_year: int) -> List[float]:
    if data.first_year > from_year:
        return data.monthly
    if data.last_year < from_year:
        return []

    months_diff = (from_year - data.first_year) * 12
    return data.monthly[months_diff::]

def get_max_first_year(data_list: Iterable[StockReturns]):
    return max([x.first_year for x in data_list])

def get_correlation_between(stock1: StockReturns, stock2: StockReturns):
    data = [stock1, stock2]
    max_first_year = max([x.first_year for x in data])
    monthly = [np.array(get_monthly_from_year(x, max_first_year)) for x in data]
    assert(len(monthly[0]) == len(monthly[1]))

    return np.corrcoef(monthly)[0][1]


def get_correlation_table_view(stocks: OrderedDict[str, StockReturns]) -> List[List[str]]:
    stock_names = list(stocks.keys())

    corr_table = [['-'] * len(stock_names) for _ in stock_names]
    for i in range(0, len(stock_names)):
        for i2 in range(0, len(stock_names)):
            if i != i2:
                corr = get_correlation_between(stocks[stock_names[i2]], stocks[stock_names[i]])
                corr_table[i2][i] = f'{round(corr * 100, 2)}%'

    return corr_table

def get_max_returns_from_same_year(data_list: Iterable[StockReturns]) -> NDArray[np.floating[Any]]:
    max_first_year = get_max_first_year(data_list)
    return np.array([get_monthly_from_year(x, max_first_year) for x in data_list])

def calc_returns_amount(amount: float, percent: float):
    return amount * (1 + percent / 100)

def calc_returns_amount_list(init_amount: float, percents: List[float]):
    amounts: List[float] = []
    for percent in percents:
        prev_amount = amounts[-1] if len(amounts) else init_amount
        amounts.append(calc_returns_amount(amount=prev_amount, percent=percent))
    return amounts

def from_monthly_std_to_annual(month_std):
    return month_std * np.sqrt(12)

def get_stocks_std_view(stocks: OrderedDict[str, StockReturns]) -> List[str]:
    return [f'{round(from_monthly_std_to_annual(np.std(x.monthly)), 2)}%' for x in stocks.values()]