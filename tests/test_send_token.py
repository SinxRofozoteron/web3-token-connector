from typing import Callable
from unittest.mock import MagicMock

from eth_tester import EthereumTester

from src.wallet import Wallet


class TestSendToken:

    test_token_address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"

    def test_calls_contract_transfer_function(
        self,
        wallet: Wallet,
        eth_tester: EthereumTester,
        transfer_mock: MagicMock,
        get_wait_for_transaction_receipt_mock: Callable,
    ):
        test_to_account = eth_tester.get_accounts()[1]
        test_amount = 10000000

        wallet.send_token(self.test_token_address, test_to_account, test_amount)
        transfer_mock.assert_called_once_with(test_to_account, test_amount)

    def test_calls_estimate_gas_with_correct_params(
        self,
        wallet: Wallet,
        eth_tester: EthereumTester,
        transfer_mock: MagicMock,
        get_wait_for_transaction_receipt_mock: Callable,
        get_estimate_gas_mock: Callable[[str], MagicMock],
    ):
        test_to_account = eth_tester.get_accounts()[1]
        test_amount = 10000000
        estimate_gas_mock: MagicMock = get_estimate_gas_mock(transfer_mock)

        wallet.send_token(self.test_token_address, test_to_account, test_amount)
        estimate_gas_mock.assert_called_with({"from": wallet.address})

    def test_returns_tx_receipt(
        self,
        wallet: Wallet,
        eth_tester: EthereumTester,
        transfer_mock: MagicMock,
        get_wait_for_transaction_receipt_mock: Callable,
    ):
        test_to_account = eth_tester.get_accounts()[1]
        test_amount = 10000000
        test_tx_receipt = "Test Transaction Receipt"
        get_wait_for_transaction_receipt_mock(test_tx_receipt)

        tx_receipt = wallet.send_token(
            self.test_token_address, test_to_account, test_amount
        )
        assert tx_receipt == test_tx_receipt, "Did not return expected tx_receipt"
