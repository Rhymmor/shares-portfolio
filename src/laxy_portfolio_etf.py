from functools import reduce
from typing import List, TypeVar

from src.domain.stock_returns import StockReturns

L = TypeVar("L")


def flatten(arr: List[List[L]]) -> List[L]:
    return reduce(lambda x, y: x + y, arr)


def get_returns_data(txt_file: str) -> StockReturns:
    with open(txt_file, "r") as f:
        raw_text = f.read()
        lines = [x for x in raw_text.split("\n") if x != ""]
        year_rows = [x.split("\t") for x in lines if "\t" in x]

        return StockReturns(
            annual=[float(x[0]) for x in year_rows][::-1],
            annual_infl_adj=[float(x[1]) for x in year_rows][::-1],
            monthly=[float(y) for y in flatten([x[2::] for x in year_rows])][::-1],
            first_year=int(lines[-2]),
            last_year=int(lines[0]),
        )
