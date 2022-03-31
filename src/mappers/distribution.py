from typing import Any, Dict, List
from src.data.shares import SHARES_INFO
from src.domain.distribution import FundsDistribution, SharesCategoriesDistribution
from src.domain.share_type import BondInfo, Cap, Region, ShareType, StockInfo, Term


def map_funds_distribution_to_categories(
    funds: FundsDistribution,
) -> SharesCategoriesDistribution:
    by_type: Dict[ShareType, float] = {}
    by_region: Dict[Region, float] = {}
    by_cap: Dict[Cap, float] = {}
    by_term: Dict[Term, float] = {}

    for fund_name, fund_distr in funds.funds.items():
        fund_info = SHARES_INFO[fund_name]

        # TODO: remove duplications
        if fund_info.type:
            if fund_info.type not in by_type:
                by_type[fund_info.type] = 0.0
            by_type[fund_info.type] += fund_distr

        if fund_info.region:
            if fund_info.region not in by_region:
                by_region[fund_info.region] = 0.0
            by_region[fund_info.region] += fund_distr

        if isinstance(fund_info, BondInfo):
            if fund_info.term:
                if fund_info.term not in by_term:
                    by_term[fund_info.term] = 0.0
                by_term[fund_info.term] += fund_distr
        elif isinstance(fund_info, StockInfo):
            if fund_info.cap:
                if fund_info.cap not in by_cap:
                    by_cap[fund_info.cap] = 0.0
                by_cap[fund_info.cap] += fund_distr

    categories: List[Dict[Any, float]] = [by_type, by_region, by_cap, by_term]
    for category in categories:
        _normalize_distribution(category=category)

    return SharesCategoriesDistribution(
        by_type=by_type,
        by_term=by_term,
        by_cap=by_cap,
        by_region=by_region,
    )


def _normalize_distribution(category: Dict[Any, float]):
    category_sum = sum(category.values())
    for name in category.keys():
        category[name] /= category_sum
