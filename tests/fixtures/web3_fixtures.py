import pytest
from eth_tester import EthereumTester
from web3 import EthereumTesterProvider

from .types import TEthAccount


@pytest.fixture(scope="function")
def eth_tester() -> EthereumTester:
    """EthereumTester instance."""
    tester = EthereumTester()
    return tester


@pytest.fixture(scope="function")
def provider(eth_tester: EthereumTester) -> EthereumTesterProvider:
    """Mock web3 provider."""
    provider = EthereumTesterProvider(eth_tester)
    return provider


@pytest.fixture(scope="function")
def eth_account(eth_tester: EthereumTester) -> TEthAccount:
    """Test Ethereum account."""
    private_key = "0x58d23b55bc9cdce1f18c2500f40ff4ab7245df9a89505e9b1fa4851f623d241d"
    address = eth_tester.add_account(private_key)
    return {"address": address, "private_key": private_key}


__all__ = ["provider", "eth_tester", "eth_account"]
