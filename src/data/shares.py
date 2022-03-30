

from collections import OrderedDict
from typing import Dict, Optional
from src.domain.share_data import ShareData
from src.domain.stock_returns import StockReturns
from src.laxy_portfolio_etf import get_returns_data
from src.domain.share_type import AnyShareInfo, StockInfo, Region, Cap, Term, BondInfo

SHARES = OrderedDict({
    "VTI": ShareData(
        returns=get_returns_data("data/monthly-returns/vti-returns-monthly.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "VTV": ShareData(
        returns=get_returns_data("data/monthly-returns/VTV-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "S&P 500": ShareData(
        returns=get_returns_data("data/monthly-returns/s&p_500-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "EAFE": ShareData(
        returns=get_returns_data("data/monthly-returns/eafe-returns-monthly.txt"),
        info=StockInfo(region=Region.ExUS, cap=Cap.Large),
    ),
    "VUG": ShareData(
        returns=get_returns_data("data/monthly-returns/vug-returns.txt"),
        info=StockInfo( region=Region.US, cap=Cap.Large),
    ),
    "Russell 2000": ShareData(
        returns=get_returns_data("data/monthly-returns/russell_2000-returns-monthly.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Small),
    ),
    "IJS": ShareData(
        returns=get_returns_data("data/monthly-returns/IJS-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Small),
    ),
    "EAFE Small-Cap": ShareData(
        returns=get_returns_data("data/monthly-returns/eafe-small-cap-return-monthly.txt"),
        info=StockInfo(region=Region.ExUS, cap=Cap.Small),
    ),
    "VNQ (REIT)": ShareData(
        returns=get_returns_data("data/monthly-returns/vnq-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "GLD": ShareData(
        returns=get_returns_data("data/monthly-returns/gld-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "DBC": ShareData(
        returns=get_returns_data("data/monthly-returns/dbc-returns.txt"),
        info=StockInfo(region=Region.US, cap=Cap.Large),
    ),
    "BND": ShareData(
        returns=get_returns_data("data/monthly-returns/bnd-returns.txt"),
        info=BondInfo(region=Region.US, term=Term.Long),
    ),
    "TIP": ShareData(
        returns=get_returns_data("data/monthly-returns/TIP-returns.txt"),
        info=BondInfo(region=Region.US, term=Term.Long),
    ),
    "SHY": ShareData(
        returns=get_returns_data("data/monthly-returns/shy-returns.txt"),
        info=BondInfo(region=Region.US, term=Term.Short),
    ),
})

def _get_shares_data() -> OrderedDict[str, StockReturns]:
    data: OrderedDict[str, StockReturns] = OrderedDict({})
    for (share_name, share) in SHARES.items():
        data[share_name] = share.returns

    return data

def _get_shares_info() -> OrderedDict[str, AnyShareInfo]:
    data: OrderedDict[str, AnyShareInfo] = OrderedDict({})
    for (share_name, share) in SHARES.items():
        data[share_name] = share.info

    return data

SHARES_DATA: OrderedDict[str, StockReturns] = _get_shares_data()
SHARES_INFO: OrderedDict[str, AnyShareInfo] = _get_shares_info()
