from typing import Dict, List, Union
from collections import OrderedDict

import numpy as np
from src.domain.share_type import BondInfo, StockInfo
from src.domain.distribution import SharesDistribution
from src.domain.stock_returns import StockReturns
from src.statistics import calc_weighted_annual_std, calc_weighted_annual_returns


def share_to_percent(share: float):
    return f'{round(share * 100, 2)}%'

def prepare_stock_table_rows(flatten_portfolio: list) -> List[List[str]]:
    stocks_table: List[List[str]] = []

    full_share = 0
    for row in flatten_portfolio:
        full_share += row["share"]

    for stock in flatten_portfolio:
        share = stock["share"]
        stocks_table.append([
            share_to_percent(share / full_share),
            share_to_percent(share)
        ])

    return stocks_table

def get_stock_name(share: dict):
    return f'{share["region"].capitalize()} {share["cap"].capitalize()}-cap stocks'

def get_fund_distribution(
    funds: List[Dict[str, float]],
    info: OrderedDict[str, Union[StockInfo, BondInfo]],
    distrib: SharesDistribution
) -> OrderedDict[str, float]:
    merged_funds: Dict[str, float] = {}
    for funds_type in funds:
        merged_funds = merged_funds | funds_type

    funds_distibution: Dict[str, float] = {}

    for fund_name, fund_distrib in merged_funds.items():
        value: float = fund_distrib

        fund_info = info[fund_name]
        value *= distrib.by_type[getattr(fund_info, 'type')]
        if isinstance(fund_info, StockInfo):
            value *= distrib.by_cap[fund_info.cap] * distrib.by_region[fund_info.region]
        if isinstance(fund_info, BondInfo):
            value *= distrib.by_term[fund_info.term]

        funds_distibution[fund_name] = value

    return OrderedDict(funds_distibution)

def calc_portfolio_std(distribution: OrderedDict[str, float], data: OrderedDict[str, StockReturns]):
    portfolio_data: Dict[str, StockReturns] = OrderedDict()
    for fund_name in distribution.keys():
        portfolio_data[fund_name] = data[fund_name]
    return calc_weighted_annual_std(data = portfolio_data, weights=list(distribution.values()))

def calc_portfolio_returns(distribution: OrderedDict[str, float], data: OrderedDict[str, StockReturns]):
    portfolio_data: Dict[str, StockReturns] = OrderedDict()
    for fund_name in distribution.keys():
        portfolio_data[fund_name] = data[fund_name]
    return calc_weighted_annual_returns(data = portfolio_data, weights=list(distribution.values()))