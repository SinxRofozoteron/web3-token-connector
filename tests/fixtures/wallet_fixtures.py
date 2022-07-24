import pytest

from src.wallet import Wallet

from .types import TEthAccount


@pytest.fixture(scope="function")
def wallet(provider, eth_account: TEthAccount):
    wallet = Wallet(provider, eth_account["address"], eth_account["private_key"])
    return wallet


__all__ = ["wallet"]
