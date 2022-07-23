from typing import TypedDict


class TEthAccount(TypedDict):

    address: str
    private_key: str


__all__ = ["TEthAccount"]
