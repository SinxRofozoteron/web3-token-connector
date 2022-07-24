from typing import Callable
from unittest.mock import MagicMock

from src.wallet import Wallet

from .fixtures import TEthAccount


class TestGetTokenBalance:

    test_token_address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"

    def test_calls_balanceOf_for_provided_wallet_address(
        self, wallet: Wallet, eth_account: TEthAccount, balanceOf_mock: MagicMock
    ):
        wallet.get_token_balance(self.test_token_address)
        balanceOf_mock.assert_called_once_with(eth_account["address"])

    def test_calls_call_on_balanceOf_function(
        self,
        wallet: Wallet,
        balanceOf_mock: MagicMock,
        get_function_call_mock: Callable[[MagicMock], MagicMock],
    ):
        call_mock = get_function_call_mock(balanceOf_mock)
        wallet.get_token_balance(self.test_token_address)
        call_mock.assert_called_once()

    def test_returns_balance(
        self,
        wallet: Wallet,
        balanceOf_mock: MagicMock,
        get_function_call_mock: Callable[[MagicMock], MagicMock],
    ):
        test_balance = "100000005432"
        get_function_call_mock(balanceOf_mock, return_value=test_balance)

        balance = wallet.get_token_balance(self.test_token_address)
        assert balance == test_balance, "Did not return correct balance"
