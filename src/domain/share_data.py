from dataclasses import dataclass
from src.domain.share_type import AnyShareInfo
from src.domain.stock_returns import StockReturns


@dataclass
class ShareData:
    returns: StockReturns
    info: AnyShareInfo
