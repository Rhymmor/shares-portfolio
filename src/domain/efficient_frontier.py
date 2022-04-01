from dataclasses import dataclass
from typing import List
from numpy import float64
from numpy.typing import NDArray


@dataclass
class FrontierPoint:
    volatility: float
    returns: float
    sharpe_ratio: float
    weights: NDArray[float64]


@dataclass
class EfficientFrontier:
    points: List[FrontierPoint]
