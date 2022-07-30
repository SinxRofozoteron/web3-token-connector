from typing import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from web3.contract import ContractFunctions

from src.wallet import Wallet
from tokens import ABI


@pytest.fixture(scope="function")
def balanceOf_mock(mocker: MockerFixture, wallet: Wallet) -> MagicMock:
    """Creates mock for ERC20 contract balanceOf function."""

    balanceOf_mock = mocker.stub()
    address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"
    functions = ContractFunctions(abi=ABI, address=address, web3=wallet.web3)
    mocker.patch.object(functions, "balanceOf", new=balanceOf_mock)
    contract_mock = wallet.web3.eth.contract(wallet.web3.toChecksumAddress(address))
    mocker.patch.object(contract_mock, "functions", new=functions)
    mocker.patch.object(wallet.web3.eth, "contract", return_value=contract_mock)
    return balanceOf_mock


@pytest.fixture(scope="function")
def transfer_mock(mocker: MockerFixture, wallet: Wallet) -> MagicMock:
    """Creates mock for ERC20 contract transfer function."""

    transfer_mock = mocker.stub()
    address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"
    functions = ContractFunctions(abi=ABI, address=address, web3=wallet.web3)
    mocker.patch.object(functions, "transfer", new=transfer_mock)
    contract_mock = wallet.web3.eth.contract(wallet.web3.toChecksumAddress(address))
    mocker.patch.object(contract_mock, "functions", new=functions)
    mocker.patch.object(wallet.web3.eth, "contract", return_value=contract_mock)
    return transfer_mock


@pytest.fixture(scope="function")
def get_function_call_mock(mocker: MockerFixture) -> Callable[[Callable], MagicMock]:
    """Helper with mocking contract function call method.

    Example
    -------
      def test(balanceOf_mock, get_function_call_mock):
        call_mock = get_function_call_mock(balanceOf_mock)

        test_token_address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"
        wallet.get_token_balance(test_token_address)

        # Verify contract.functions.balanceOf(self.address).call() call
        assert call_mock.assert_called_once()

    Return
    ------
      Wrapper function that wraps around another function and
      returns a mock of call().
    """

    def create_mock(
        contract_function: MagicMock, return_value: any = None
    ) -> MagicMock:
        """Creates mock for call() function on contract function result.

        Args:
            contract_function (MagicMock): mock of contract function
            return_value (any, optional): Mock value for call functio to return.
              Defaults to None.

        Returns:
            MagicMock
        """
        call_mock: MagicMock = mocker.stub("call_mock")
        call_mock.return_value = return_value

        class FunctionReturnMock:
            call = call_mock

        contract_function.return_value = FunctionReturnMock
        return call_mock

    return create_mock


@pytest.fixture(scope="function")
def get_estimate_gas_mock(mocker: MockerFixture) -> Callable[[Callable], MagicMock]:
    """Helper with mocking contract function estimate_gas method.

    Example
    -------
      def test(send_token_mock, get_estimate_gas_mock, wallet):
        estimate_gas_mock = get_estimate_gas_mock(send_token_mock)

        wallet.send_token(test_address, test_to_account, test_amount)

        # Verify contract.functions.transfer(to_address, amount).estimate_gas() call
        assert estimate_gas_mock.assert_called_once()

    Return
    ------
      Wrapper function that wraps around another function and
      returns a mock of call().
    """
    estimate_gas_mock = mocker.stub("estimate_gas_mock")

    class FunctionReturnMock:
        estimate_gas = estimate_gas_mock

    def create_mock(
        contract_function: MagicMock, return_value: any = None
    ) -> MagicMock:
        """Creates mock for estimate_gas() function on contract function result.

        Args:
            contract_function (MagicMock): mock of contract function
            return_value (any, optional):
              Mock value for estimate_gas function to return.
              Defaults to None.

        Returns:
            MagicMock
        """
        estimate_gas_mock.return_value = return_value
        contract_function.return_value = FunctionReturnMock
        return estimate_gas_mock

    return create_mock


@pytest.fixture(scope="function")
def get_build_transaction_mock(
    mocker: MockerFixture,
) -> Callable[[Callable], MagicMock]:
    """Helper with mocking contract function build_transaction method.

    Example
    -------
      def test(send_token_mock, get_build_transaction_mock, wallet):
        build_transaction_mock = get_build_transaction_mock(send_token_mock)

        wallet.send_token(test_address, test_to_account, test_amount)

        # Verify contract.functions.transfer(
        #          to_address, amount
        #        ).build_transaction() call
        assert build_transaction_mock.assert_called_once()

    Return
    ------
      Wrapper function that wraps around another function and
      returns a mock of call().
    """
    build_transaction_mock = mocker.stub("build_transaction_mock")

    class FunctionReturnMock:
        build_transaction = build_transaction_mock

    def create_mock(function: MagicMock, return_value: any = None) -> MagicMock:
        """Creates mock for build_transaction() function on contract function result.

        Args:
            function (MagicMock): mock
            return_value (any, optional):
              Mock value for build_transaction function to return.
              Defaults to None.

        Returns:
            MagicMock
        """
        build_transaction_mock.return_value = return_value
        function.return_value = FunctionReturnMock
        return build_transaction_mock

    return create_mock


__all__ = [
    "balanceOf_mock",
    "get_function_call_mock",
    "transfer_mock",
    "get_estimate_gas_mock",
    "get_build_transaction_mock",
]
