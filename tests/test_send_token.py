# from typing import Callable
# from unittest.mock import MagicMock
# import pytest

# from eth_tester import EthereumTester

# from src.wallet import Wallet

# @pytest.fixture(scope='function')
# def setup_and_get_test_data(
#     eth_tester: EthereumTester,
#     wallet: Wallet,
#     transfer_mock: MagicMock,
#     get_wait_for_transaction_receipt_mock: Callable,
#     get_fee_history_mock: Callable,
#     get_estimate_gas_mock: Callable,
#     get_build_transaction_mock: Callable
# ):
#     get_fee_history_mock()
#     estimate_gas_mock = get_estimate_gas_mock(transfer_mock)
#     amount = 10000000
#     get_build_transaction_mock(estimate_gas_mock, return_value={
#         'from': wallet.address,
#         'value': amount,
#         'gas': 1000
#     })
#     test_tx_receipt = "Test Transaction Receipt"
#     get_wait_for_transaction_receipt_mock(test_tx_receipt)
#     to_account = eth_tester.get_accounts()[1]
#     token_address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"

#     return to_account, amount, token_address, estimate_gas_mock, test_tx_receipt


# class TestSendToken:

#     def test_calls_contract_transfer_function(
#         self,
#         setup_and_get_test_data,
#         wallet: Wallet,
#         transfer_mock: MagicMock,
#     ):
# (
#     test_to_account, test_amount, test_token_address, _, _
# ) = setup_and_get_test_data
#         wallet.send_token(test_token_address, test_to_account, test_amount)
#         transfer_mock.assert_called_once_with(test_to_account, test_amount)

#     def test_calls_estimate_gas_with_correct_params(
#         self,
#         setup_and_get_test_data,
#         wallet: Wallet,

#     ):
# (
#     test_to_account, test_amount, test_token_address, estimate_gas_mock, _
#     ) = setup_and_get_test_data

#         wallet.send_token(test_token_address, test_to_account, test_amount)
#         estimate_gas_mock.assert_called_with({"from": wallet.address})

#     def test_returns_tx_receipt(
#         self,
#         setup_and_get_test_data,
#         wallet: Wallet
#     ):
# (
#     test_to_account, test_amount, test_token_address, _, test_tx_receipt
#     ) = setup_and_get_test_data

#         tx_receipt = wallet.send_token(
#             test_token_address, test_to_account, test_amount
#         )
#         assert tx_receipt == test_tx_receipt, "Did not return expected tx_receipt"
