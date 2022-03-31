from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class ShareType(Enum):
    Stock = "stock"
    Bond = "bond"


class Region(Enum):
    US = "US"
    ExUS = "ex-US"


class Cap(Enum):
    Large = "large"
    Small = "small"


class Term(Enum):
    Short = "short"
    Long = "long"


@dataclass
class ShareInfo:
    type: Optional[ShareType]
    region: Region = Region.US


@dataclass
class StockInfo(ShareInfo):
    cap: Cap = Cap.Large
    type: Optional[ShareType] = ShareType.Stock


@dataclass
class BondInfo(ShareInfo):
    term: Term = Term.Long
    type: Optional[ShareType] = ShareType.Bond


AnyShareInfo = Union[StockInfo, BondInfo]
