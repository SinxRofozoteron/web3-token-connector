from typing import Callable
from unittest.mock import MagicMock

import pytest
from web3.types import FeeHistory

from src.wallet import Wallet


class TestEstimateGasFee:

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

    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    def test_returns_amount_in_wei_if_priority_specified(
        self,
        priority,
        wallet: Wallet,
        get_fee_history_mock: Callable[[FeeHistory], MagicMock],
    ):
        get_fee_history_mock(self.test_fee_history)

        estimated_fee = wallet.estimate_gas_fee(priority)
        assert isinstance(estimated_fee, float), "Did not return an integer."

    def test_returns_dict_if_no_priority_specified(
        self, wallet: Wallet, get_fee_history_mock: Callable[[FeeHistory], MagicMock]
    ):
        get_fee_history_mock(self.test_fee_history)

        estimated_fee: dict = wallet.estimate_gas_fee()
        assert isinstance(estimated_fee, dict), "Did not return a dict."

    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    def test_returns_dict_with_correct_keys_and_values_if_no_priority_specified(
        self,
        priority,
        wallet: Wallet,
        get_fee_history_mock: Callable[[FeeHistory], MagicMock],
    ):
        get_fee_history_mock(self.test_fee_history)

        estimated_fee: dict = wallet.estimate_gas_fee()

        assert (
            priority in estimated_fee.keys()
        ), f"Returned dict does not have '{priority}' key."
        assert isinstance(
            estimated_fee[priority], float
        ), f"Value for '{priority}' priority is not a float."
