from collections import OrderedDict
import yaml
from src.domain.distribution import FundsDistribution, SharesDistribution


def import_portfolio(file_path: str) -> SharesDistribution:
    with open(file_path, "r") as f:
        funds = OrderedDict(yaml.safe_load(f.read()))
        shares = FundsDistribution(funds=funds)

        return SharesDistribution(shares=shares)
