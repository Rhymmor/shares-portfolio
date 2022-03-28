

from dataclasses import dataclass
from typing import Dict

from src.domain.share_type import Cap, Region, ShareType, Term

@dataclass
class SharesDistribution:
    by_type: Dict[ShareType, float]
    by_region: Dict[Region, float]
    by_cap: Dict[Cap, float]
    by_term: Dict[Term, float]