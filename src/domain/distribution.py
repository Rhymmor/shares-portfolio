from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, OrderedDict, Union
import numpy as np
from numpy.typing import NDArray
from src.data.shares import SHARES

from src.domain.share_type import Cap, Region, ShareType, Term


@dataclass
class SharesCategoriesDistribution:
    by_type: Dict[ShareType, float]
    by_region: Dict[Region, float]
    by_cap: Dict[Cap, float]
    by_term: Dict[Term, float]

    def __post_init__(self):
        obj = asdict(self)
        for name, category in obj.items():
            assert np.isclose(
                sum(category.values()), 1.0
            ), f'Sum in category "{name}" is not equal to 100% {sum(category.values()) * 100}%) for {category}'


@dataclass
class FundsDistribution:
    funds: OrderedDict[str, float]

    def __post_init__(self):
        funds_sum = sum(self.funds.values())
        assert np.isclose(
            funds_sum, 1.0
        ), f"A sum of funds is not equal to 100% (= {funds_sum * 100}%) for {self.funds}"

        for fund in self.funds.keys():
            assert fund in SHARES, f"No {fund} share in the global stocks dictionary"


@dataclass
class SharesDistribution:
    shares: Union[FundsDistribution, List[FundsDistribution]]
    categories: Optional[SharesCategoriesDistribution] = None

    def __post_init__(self):
        if isinstance(self.shares, list):
            assert self.categories is not None, "If shares is list there should be categories"


@dataclass
class DistributionsData:
    funds_ratio: list[OrderedDict[str, float]]
    """Percentage ratio by fund items"""
    std: List[float]
    """Standard deviation"""
    returns: List[NDArray[np.floating[Any]]]
    """Returns monthly rate"""
    annual_mean_returns: List[float]
    """Annual returns geometric mean"""
    returns_amounts: List[List[float]]
    """Monthly returns amount"""
