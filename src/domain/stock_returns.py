from dataclasses import dataclass
from typing import List


@dataclass
class StockReturns:
    annual: List[float]
    """Annual returns in percents"""
    annual_infl_adj: List[float]
    """Annual returns in percents adjusted to annual inflation"""
    monthly: List[float]
    """Monthly returns in percents"""
    first_year: int
    """Year when returns starts"""
    last_year: int
    """Year when returns ends"""