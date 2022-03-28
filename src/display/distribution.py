

from typing import Dict, List
import numpy as np
import pandas as pd
import plotly.express as px
from IPython.display import display

from src.distribution import calc_distributions_data
from src.domain.distribution import SharesDistribution
from src.plot_utils import get_monthly_data_range

def display_distributions(distribs: List[SharesDistribution], names: List[str], funds: List[Dict[str, float]]):
    distributions_data = calc_distributions_data(distribs, funds=funds)

    percent_columns = [[f'{round(x * 100, 2)}%' for x in distrib.values()] for distrib in distributions_data.funds_ratio]
    df = pd.DataFrame(np.array(percent_columns).transpose(), columns=names, index=list(distributions_data.funds_ratio[0].keys()))
    display(df)

    max_first_year = 1992

    df = pd.DataFrame(np.array([distributions_data.annual_mean_returns, distributions_data.std]).transpose(), columns=["Mean ret.", "Std"], index=names)
    display(df)

    df = pd.DataFrame(
        np.array(distributions_data.returns_amounts).transpose(),
        columns=names,
        index=get_monthly_data_range(max_first_year, 2021)
    )

    fig = px.line(df, x=df.index, y=df.columns)
    fig.show(renderer="notebook+pdf")
