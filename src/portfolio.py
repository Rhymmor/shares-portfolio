from typing import Dict, List, Optional, Union
from collections import OrderedDict

from src.domain.share_type import BondInfo, StockInfo
from src.domain.distribution import SharesDistribution
from src.domain.stock_returns import StockReturns
from src.statistics import calc_weighted_annual_std, calc_weighted_annual_returns


def share_to_percent(share: float):
    return f"{round(share * 100, 2)}%"


def prepare_stock_table_rows(flatten_portfolio: list) -> List[List[str]]:
    stocks_table: List[List[str]] = []

    full_share = 0
    for row in flatten_portfolio:
        full_share += row["share"]

    for stock in flatten_portfolio:
        share = stock["share"]
        stocks_table.append([share_to_percent(share / full_share), share_to_percent(share)])

    return stocks_table


def get_stock_name(share: dict):
    return f'{share["region"].capitalize()} {share["cap"].capitalize()}-cap stocks'


def get_fund_distribution(
    distrib: SharesDistribution,
    info: OrderedDict[str, Union[StockInfo, BondInfo]],
) -> OrderedDict[str, float]:
    funds, categories = distrib.shares, distrib.categories

    merged_funds: OrderedDict[str, float] = OrderedDict() if isinstance(funds, list) else funds.funds

    if isinstance(funds, list):
        for funds_type in funds:
            merged_funds = OrderedDict(merged_funds | funds_type.funds)

    funds_distibution: OrderedDict[str, float] = OrderedDict({})

    for fund_name, fund_distrib in merged_funds.items():
        value: float = fund_distrib

        fund_info = info[fund_name]

        if categories:
            value *= categories.by_type[getattr(fund_info, "type")]
            if isinstance(fund_info, StockInfo):
                value *= categories.by_cap[fund_info.cap] * categories.by_region[fund_info.region]
            if isinstance(fund_info, BondInfo):
                value *= categories.by_term[fund_info.term]

        funds_distibution[fund_name] = value

    return funds_distibution


def calc_portfolio_std(funds_distribution: OrderedDict[str, float], data: OrderedDict[str, StockReturns]):
    portfolio_data: Dict[str, StockReturns] = OrderedDict()
    for fund_name in funds_distribution.keys():
        portfolio_data[fund_name] = data[fund_name]
    return calc_weighted_annual_std(data=portfolio_data, weights=list(funds_distribution.values()))


def calc_portfolio_returns(
    funds_distribution: OrderedDict[str, float],
    data: OrderedDict[str, StockReturns],
    from_year: Optional[int] = None,
):
    portfolio_data: Dict[str, StockReturns] = OrderedDict()
    for fund_name in funds_distribution.keys():
        portfolio_data[fund_name] = data[fund_name]
    return calc_weighted_annual_returns(
        data=portfolio_data,
        weights=list(funds_distribution.values()),
        from_year=from_year,
    )
