import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from IPython.display import display

from src.domain.distribution import DistributionsData
from src.domain.efficient_frontier import EfficientFrontier


def display_efficient_frontier(ef: EfficientFrontier, portfolio_data: DistributionsData):
    volatility = [x.volatility for x in ef.points]
    returns = [x.returns for x in ef.points]
    sharpe = np.array([x.sharpe_ratio for x in ef.points])

    index_sharpe_max = sharpe.argmax()
    df = pd.DataFrame(
        {
            "Volatility": volatility,
            "Return": returns,
            "Sharpe ratio": sharpe,
            "Index": [i for (i, _) in enumerate(volatility)],
        }
    )

    fig = px.scatter(
        df,
        x="Volatility",
        y="Return",
        color="Sharpe ratio",
        hover_data=["Volatility", "Return", "Sharpe ratio", "Index"],
        opacity=0.3,
    )
    add_marker(
        fig,
        name="Best Sharpe",
        vol=volatility[index_sharpe_max],
        ret=returns[index_sharpe_max],
        sharpe=sharpe[index_sharpe_max],
        index=index_sharpe_max,
    )
    add_marker(
        fig,
        name="Portfolio",
        vol=portfolio_data.std[0],
        ret=portfolio_data.annual_mean_returns[0],
        sharpe=portfolio_data.annual_mean_returns[0] / portfolio_data.std[0],
    )

    display(fig)


def add_marker(fig, name, vol: float, ret: float, sharpe: float, index=None):
    fig.add_scatter(
        name=name,
        x=[vol],
        y=[ret],
        opacity=1,
        showlegend=False,
        mode="markers",
        customdata=[[sharpe, index or ""]],
        hovertemplate="""
Volatility=%{x}<br>
Return=%{y}<br>
Sharpe ratio=%{customdata[0]}<br>
Index=%{customdata[1]}
        """,
        marker=go.scatter.Marker(color="black", symbol="square", size=10),  # type: ignore
    )

    return fig
