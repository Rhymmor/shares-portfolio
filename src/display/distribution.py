from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
from IPython.display import display

from src.distribution import calc_distributions_data
from src.domain.distribution import DistributionsData, SharesDistribution
from src.plot_utils import get_monthly_data_range


def display_distributions(distribs: List[SharesDistribution], names: List[str]):
    distributions_data = calc_distributions_data(distribs=distribs)

    display_distributions_table(names, distributions_data=distributions_data)

    max_first_year = 1992

    df = pd.DataFrame(
        np.array(distributions_data.returns_amounts).transpose(),
        columns=names,
        index=get_monthly_data_range(max_first_year, 2021),
    )

    fig = px.line(df, x=df.index, y=df.columns)
    fig.show(renderer="notebook+pdf")


def display_distributions_table(
    names: List[str],
    distributions_data: Optional[DistributionsData] = None,
    distribs: Optional[List[SharesDistribution]] = None,
):
    if distributions_data is None and distribs is not None:
        distributions_data = calc_distributions_data(distribs=distribs)

    if distributions_data is None:
        raise ValueError("Neither distributions_data nor distribs were provided")

    percent_columns = [
        [f"{round(x * 100, 2)}%" for x in distrib.values()]
        + ["-", f"{distributions_data.annual_mean_returns[i]}", f"{distributions_data.std[i]}"]
        for (i, distrib) in enumerate(distributions_data.funds_ratio)
    ]

    index = [*distributions_data.funds_ratio[0].keys(), "-", "Mean ret.", "Std"]
    df = pd.DataFrame(
        np.array(percent_columns).transpose(),
        columns=names,
        index=index,
    )
    display(df)
