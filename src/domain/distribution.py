

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, OrderedDict
import numpy as np
from numpy.typing import NDArray

from src.domain.share_type import Cap, Region, ShareType, Term

@dataclass
class SharesDistribution:
    by_type: Dict[ShareType, float]
    by_region: Dict[Region, float]
    by_cap: Dict[Cap, float]
    by_term: Dict[Term, float]

    def __post_init__(self):
        obj = asdict(self)
        for category in obj.values():
            assert(sum(category.values()) == 1)

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