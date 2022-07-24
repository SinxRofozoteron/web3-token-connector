from typing import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from web3.contract import ContractFunctions

from src.wallet import Wallet
from tokens import ABI


@pytest.fixture(scope="function")
def balanceOf_mock(mocker: MockerFixture, wallet: Wallet):
    """Creates mock for ERC20 contract balanceOf function."""

    balanceOfMock = mocker.stub()
    address = "0x0f5d2fb29fb7d3cfee444a200298f468908cc942"
    functions = ContractFunctions(abi=ABI, address=address, web3=wallet.web3)
    mocker.patch.object(functions, "balanceOf", new=balanceOfMock)
    contract_mock = wallet.web3.eth.contract(wallet.web3.toChecksumAddress(address))
    mocker.patch.object(contract_mock, "functions", new=functions)
    mocker.patch.object(wallet.web3.eth, "contract", return_value=contract_mock)
    return balanceOfMock


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
            _type_: _description_
        """
        call_mock: MagicMock = mocker.stub("call_mock")
        call_mock.return_value = return_value

        class FunctionReturnMock:
            call = call_mock

        contract_function.return_value = FunctionReturnMock
        return call_mock

    return create_mock


__all__ = ["balanceOf_mock", "get_function_call_mock"]
