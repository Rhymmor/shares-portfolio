from dataclasses import dataclass

from src.domain.numbers_utils import FloatList


@dataclass
class StockReturns:
    annual: FloatList
    """Annual returns in percents"""
    annual_infl_adj: FloatList
    """Annual returns in percents adjusted to annual inflation"""
    monthly: FloatList
    """Monthly returns in percents"""
    first_year: int
    """Year when returns starts"""
    last_year: int
    """Year when returns ends"""
