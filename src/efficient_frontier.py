from collections import OrderedDict
from typing import List
import numpy as np
from numpy.typing import NDArray
from src.domain.distribution import FundsDistribution, SharesDistribution

from src.domain.stock_returns import StockReturns
from src.domain.efficient_frontier import EfficientFrontier, FrontierPoint
from src.statistics import (
    calc_annual_geometric_mean_from_monthly,
    calc_weighted_annual_std,
    calc_weighted_monthly_returns,
)


def calculate_efficient_frontier(
    shares: OrderedDict[str, StockReturns], from_year=1992, seed=23, portfolio_num=10000
) -> EfficientFrontier:
    stocks_num = len(shares.keys())

    np.random.seed(seed)
    num_ports = portfolio_num
    points: List[FrontierPoint] = []

    for _ in range(num_ports):
        # Weights
        weights: NDArray[np.float64] = np.array(np.random.random(stocks_num))
        weights = weights / np.sum(weights)

        # Expected return
        weighted_returns, year = calc_weighted_monthly_returns(shares, weights, from_year)
        vol = calc_weighted_annual_std(shares, weights)
        ret = calc_annual_geometric_mean_from_monthly(weighted_returns)

        points.append(FrontierPoint(volatility=vol, returns=ret, sharpe_ratio=ret / vol, weights=weights))

    return EfficientFrontier(points=points)


def get_max_return_points_by_volatility_limits(
    ef: EfficientFrontier, vol_limits: List[int]
) -> OrderedDict[int, FrontierPoint]:
    point_dict: OrderedDict[int, FrontierPoint] = OrderedDict()
    for vol in vol_limits:
        point_dict[vol] = None  # type: ignore

    for point in ef.points:
        for vol_limit in vol_limits:
            old_point = point_dict.get(vol_limit, None)
            if point.volatility < vol_limit:
                if old_point is None or old_point.returns < point.returns:
                    point_dict[vol_limit] = point

    return point_dict


def get_point_distribution(point: FrontierPoint, stock_names: List[str]):
    funds = OrderedDict([(stock_names[x[0]], x[1]) for x in enumerate(point.weights)])
    return SharesDistribution(shares=FundsDistribution(funds=funds))
