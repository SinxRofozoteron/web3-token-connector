from typing import Callable
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from web3.types import FeeHistory

from src.wallet import Wallet


@pytest.fixture(scope="function")
def get_wait_for_transaction_receipt_mock(
    mocker: MockerFixture, wallet: Wallet
) -> Callable[[str], MagicMock]:
    """Helper with mocking web3 wait_for_transaction_receipt function.

    Returns:
       Callable[[str], MagicMock]: mock creator function
    """
    wait_for_transaction_receipt_mock = mocker.stub()
    mocker.patch.object(
        wallet.web3.eth,
        "wait_for_transaction_receipt",
        new=wait_for_transaction_receipt_mock,
    )

    def create_mock(return_value=None) -> MagicMock:
        """Creates wait_for_transaction_receipt_mock.

        Args:
            return_value (Any, optional):
              Value to return from wait_for_transaction_receipt.
              Defaults to None.

        Returns:
            MagicMock
        """
        wait_for_transaction_receipt_mock.return_value = return_value
        return wait_for_transaction_receipt_mock

    return create_mock


@pytest.fixture(scope="function")
def get_fee_history_mock(
    mocker: MockerFixture, wallet: Wallet
) -> Callable[[FeeHistory], MagicMock]:
    """Helper with mocking web3 fee_history function.

    Returns:
        Callable[[FeeHistory], MagicMock]: mock creator function.
    """
    fee_history_mock = mocker.stub()
    mocker.patch.object(
        wallet.web3.eth,
        "fee_history",
        new=fee_history_mock,
    )
    test_fee_history: FeeHistory = {
        "reward": [
            [10, 20, 30],
            [10, 20, 30],
            [10, 20, 30],
            [10, 20, 30],
            [10, 20, 30],
        ],
        "baseFeePerGas": [99],
    }

    def create_mock(return_value: FeeHistory = test_fee_history) -> MagicMock:
        """Creates fee_history_mock.

        Args:
            return_value (FeeHistory, optional):
              Value to return from fee_history_mock.
              Defaults to: {
                    "reward": [
                        [10, 20, 30],
                        [10, 20, 30],
                        [10, 20, 30],
                        [10, 20, 30],
                        [10, 20, 30],
                    ],
                    "baseFeePerGas": [99],
                }.

        Returns:
            MagicMock
        """
        fee_history_mock.return_value = return_value
        return fee_history_mock

    return create_mock


__all__ = ["get_wait_for_transaction_receipt_mock", "get_fee_history_mock"]
