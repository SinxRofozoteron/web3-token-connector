import pytest
from web3 import Web3
from web3.exceptions import InvalidAddress

from src.wallet import Wallet

from .fixtures import TEthAccount


@pytest.fixture
def setup_test_raises_error_if_not_connected(monkeypatch):
    """Setup test.

    Decsription
        Mock web3.isConnected to return false.
    """

    def mock_isConnected(*args):
        return False

    monkeypatch.setattr(Web3, "isConnected", mock_isConnected, raising=True)


def test_raises_error_if_not_connected(
    setup_test_raises_error_if_not_connected, provider
):
    """Test raises error if Web3 is not connected to the framework."""
    test_address = "Test Address"
    test_private_key = "Test Private Key"
    expected_error_message = "Could not connect to the network"

    with pytest.raises(ConnectionError, match=expected_error_message):
        Wallet(provider, test_address, test_private_key)


@pytest.mark.parametrize(
    "address",
    ["Invalid address string", 2, "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM"],
)
def test_raises_error_if_invalid_wallet_address_provided(
    address, provider, eth_account: TEthAccount
):
    test_private_key = eth_account["private_key"]
    expected_error_message = (
        f"Provided {address} address is not valid. Please provide valid wallet address."
    )

    with pytest.raises(InvalidAddress, match=expected_error_message):
        Wallet(provider, address, test_private_key)


def test_raises_error_if_invalid_private_key_provided(
    provider, eth_account: TEthAccount
):
    test_private_key = "0" + eth_account["private_key"]
    test_wallet_address = eth_account["address"]

    with pytest.raises(Exception):
        Wallet(provider, test_wallet_address, test_private_key)


def test_successfully_creates_wallet_instance_with_correct_params_provided(
    provider, eth_account: TEthAccount
):
    test_private_key = eth_account["private_key"]
    test_wallet_address = eth_account["address"]
    wallet = None

    try:
        wallet = Wallet(provider, test_wallet_address, test_private_key)
    except Exception as exp:
        raise AssertionError(
            "Creating Wallet instance with valid params raised an error:"
            f" {type(exp).__name__}('{exp}')"
        )
    assert wallet, "Wallet instance was not created"


def test_creates_own_instance_of_web3_and_it_is_connected(
    provider, eth_account: TEthAccount
):
    test_private_key = eth_account["private_key"]
    test_wallet_address = eth_account["address"]

    wallet = Wallet(provider, test_wallet_address, test_private_key)

    assert wallet.web3, "Could not find web3 instance on newly created wallet"
    assert wallet.web3.isConnected(), "Web3 is not connected"
