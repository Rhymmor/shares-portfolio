from typing import Callable, List, Optional, TypeVar
from src.data.shares import SHARES_INFO, SHARES_DATA
from src.domain.distribution import DistributionsData, SharesDistribution
from src.portfolio import calc_portfolio_returns, calc_portfolio_std, get_fund_distribution
from src.statistics import calc_annual_geometric_mean_from_monthly, calc_returns_amount_list
from copy import deepcopy

T = TypeVar('T')

def create_distributions_from(default_distrib: SharesDistribution, create_fn: Callable[[SharesDistribution, T], None], data: List[T]):
    return [modify_distrib(default_distrib, create_fn, x) for x in data]

def modify_distrib(default_distrib: SharesDistribution, modify_fn: Callable[[SharesDistribution, T], None], arg: T):
    distrib = deepcopy(default_distrib)
    modify_fn(distrib, arg)
    return distrib

def calc_distributions_data(
    distribs: List[SharesDistribution],
    init_amount=1000,
    from_year: Optional[int] = None
) -> DistributionsData:
    distributions_by_fund = [get_fund_distribution(x, SHARES_INFO) for x in distribs]
    distributions_returns = [calc_portfolio_returns(x, SHARES_DATA, from_year=from_year)[0] for x in distributions_by_fund]

    return DistributionsData(
        funds_ratio=distributions_by_fund,
        returns=distributions_returns,
        std=[round(calc_portfolio_std(x, SHARES_DATA), 2) for x in distributions_by_fund],
        annual_mean_returns=[round(
            calc_annual_geometric_mean_from_monthly(x),  # type: ignore
            2
        ) for x in distributions_returns],
        returns_amounts=[calc_returns_amount_list(init_amount, x) for x in distributions_returns]  # type: ignore
    )

