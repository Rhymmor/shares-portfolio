

from collections import OrderedDict
from IPython.display import display
import numpy as np
import plotly.express as px
import pandas as pd

from src.domain.distribution import SharesDistribution
from src.domain.stock_returns import StockReturns
from src.distribution import calc_distributions_data
from src.plot_utils import get_monthly_data_range
from src.statistics import calc_annual_geometric_mean, calc_returns_amount_list, get_max_returns_from_same_year, get_stocks_std_view


def display_portfolio(
    distrib: SharesDistribution,
    extra_stocks: OrderedDict[str, StockReturns],
):
    names = ["Portfolio"]
    max_first_year = 1992
    init_amount = 1000

    distributions_data = calc_distributions_data(
        distribs=[distrib],
        init_amount=init_amount,
        from_year=max_first_year
    )
    stock_amount_returns = [
        calc_returns_amount_list(init_amount, x) for x in get_max_returns_from_same_year(
            extra_stocks.values(),
            year=max_first_year
        )
    ]

    stocks_annual_mean = [f'{round(calc_annual_geometric_mean(x), 2)}%' for x in extra_stocks.values()]
    stocks_std_column = get_stocks_std_view(extra_stocks)

    percent_columns = [[f'{round(x * 100, 2)}%' for x in distrib.values()] for distrib in distributions_data.funds_ratio]
    df = pd.DataFrame(np.array(percent_columns).transpose(), columns=names, index=list(distributions_data.funds_ratio[0].keys()))
    display(df)


    df2 = pd.DataFrame(np.array([
            [f'{distributions_data.annual_mean_returns[0]}%', *stocks_annual_mean],
            [f'{distributions_data.std[0]}%', *stocks_std_column]
        ]).transpose(), columns=["Mean ret.", "Std"], index=[*names, *extra_stocks.keys()])
    display(df2)

    df = pd.DataFrame(
        np.array([distributions_data.returns_amounts[0], *stock_amount_returns]).transpose(),
        columns=[*names, *extra_stocks.keys()],
        index=get_monthly_data_range(max_first_year, 2021)
    )

    fig = px.line(df, x=df.index, y=df.columns)
    fig.show(renderer="notebook+pdf")