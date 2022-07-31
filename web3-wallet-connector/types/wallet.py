from typing import Literal, TypedDict

from web3.types import Wei

TPriority = Literal["low", "medium", "high"]


class TFeesByPriority(TypedDict):

    low: Wei
    medium: Wei
    high: Wei


__all__ = ["TPriority", "TFeesByPriority"]
