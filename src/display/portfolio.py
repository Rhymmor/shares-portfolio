from collections import OrderedDict
from dataclasses import asdict
from enum import Enum
from typing import Dict, List
from IPython.display import display
import numpy as np
import plotly.express as px
import pandas as pd

from src.domain.distribution import DistributionsData, SharesDistribution
from src.domain.stock_returns import StockReturns
from src.distribution import calc_distributions_data
from src.mappers.distribution import map_funds_distribution_to_categories
from src.plot_utils import get_monthly_data_range
from src.statistics import (
    calc_annual_geometric_mean,
    calc_returns_amount_list,
    get_correlation_table_view,
    get_max_returns_from_same_year,
    get_stocks_std_view,
)

names = ["Portfolio"]
DEFAULT_FIRST_YEAR = 1992
DEFAULT_LAST_YEAR = 2021
DEFAULT_INIT_AMOUNT = 1000


def display_portfolio(
    distrib: SharesDistribution,
    extra_stocks: OrderedDict[str, StockReturns],
):
    distributions_data = calc_distributions_data(
        distribs=[distrib],
        init_amount=DEFAULT_INIT_AMOUNT,
        from_year=DEFAULT_FIRST_YEAR,
    )

    display_categories_distrib_table(distrib)
    display_funds_distribution_table(distributions_data)
    display_correlation_table(distributions_data, extra_stocks, max_first_year=DEFAULT_FIRST_YEAR)
    display_porfolio_amount_figure(
        distributions_data,
        extra_stocks,
        max_first_year=DEFAULT_FIRST_YEAR,
        init_amount=DEFAULT_INIT_AMOUNT,
    )


categories_names = OrderedDict(
    {
        "by_type": "Type",
        "by_cap": "Cap",
        "by_term": "Term",
        "by_region": "Region",
    }
)


def display_categories_distrib_table(distrib: SharesDistribution):
    categories = (
        distrib.categories if isinstance(distrib.shares, list) else map_funds_distribution_to_categories(distrib.shares)
    )

    categories_dict: OrderedDict[str, Dict[Enum, float]] = OrderedDict(asdict(categories))

    index: List[str] = []
    categories_types_column: List[str] = []
    values_column: List[str] = []

    for category in categories_names.keys():
        if category in categories_dict and categories_names[category]:
            keys = categories_dict[category].keys()
            category_types_names = [x.value.capitalize() for x in keys]

            index += [categories_names[category]] + [""] * (len(category_types_names) - 1)
            categories_types_column += category_types_names
            values_column += [f"{round(categories_dict[category][x] * 100, 2)}%" for x in keys]

    df = pd.DataFrame(
        np.array([categories_types_column, values_column]).transpose(),
        columns=["", ""],
        index=index,
    )
    display(df)


def display_funds_distribution_table(distributions_data: DistributionsData):
    percent_columns = [
        [f"{round(x * 100, 2)}%" for x in distrib.values()] for distrib in distributions_data.funds_ratio
    ]
    df = pd.DataFrame(
        np.array(percent_columns).transpose(),
        columns=names,
        index=list(distributions_data.funds_ratio[0].keys()),
    )
    display(df)


def display_correlation_table(
    distributions_data: DistributionsData,
    extra_stocks: OrderedDict[str, StockReturns],
    max_first_year: int = DEFAULT_FIRST_YEAR,
):
    stocks_annual_mean = [f"{round(calc_annual_geometric_mean(x), 2)}%" for x in extra_stocks.values()]
    stocks_std_column = get_stocks_std_view(extra_stocks)
    corr_table = get_correlation_table_view(
        OrderedDict(
            {
                "Portfolio": StockReturns(
                    annual=[],
                    annual_infl_adj=[],
                    monthly=distributions_data.returns[0],
                    first_year=max_first_year,
                    last_year=2021,
                ),
                **extra_stocks,
            }
        )
    )

    index = [*names, *extra_stocks.keys()]
    splitter_column = ["|"] * len(index)

    df2 = pd.DataFrame(
        np.array(
            [
                [f"{distributions_data.annual_mean_returns[0]}%", *stocks_annual_mean],
                [f"{distributions_data.std[0]}%", *stocks_std_column],
                splitter_column,
                *corr_table,
            ]
        ).transpose(),
        columns=["Mean ret.", "Std", "|", *names, *extra_stocks.keys()],
        index=index,
    )
    display(df2)


def display_porfolio_amount_figure(
    distributions_data: DistributionsData,
    extra_stocks: OrderedDict[str, StockReturns],
    max_first_year: int = DEFAULT_FIRST_YEAR,
    init_amount: float = DEFAULT_INIT_AMOUNT,
):
    stock_amount_returns = [
        calc_returns_amount_list(init_amount, x)
        for x in get_max_returns_from_same_year(extra_stocks.values(), year=max_first_year)
    ]

    df = pd.DataFrame(
        np.array([distributions_data.returns_amounts[0], *stock_amount_returns]).transpose(),
        columns=[*names, *extra_stocks.keys()],
        index=get_monthly_data_range(max_first_year, 2021),
    )
    fig = px.line(df, x=df.index, y=df.columns)
    fig.show(renderer="notebook+pdf")
