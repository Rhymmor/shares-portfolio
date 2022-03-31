import pandas as pd


def get_monthly_data_range(from_year: int, to_year: int):
    start = f"{from_year}-01-01"
    end = f"{to_year}-12-31"
    return pd.date_range(start, end, freq="MS")
