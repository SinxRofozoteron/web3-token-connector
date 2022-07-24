from eth_typing.evm import Address
from web3 import Web3
from web3.exceptions import InvalidAddress
from web3.providers.base import BaseProvider
from web3.types import TxReceipt

from tokens import ABI


class Wallet:
    def __init__(self, provider: BaseProvider, address: Address, private_key: str):
        """Initialize Wallet.

        Args:
            provider (BaseProvider): Provider instance to pass to Web3
            address (str): wallet address
            private_key (str): wallet private key
        """
        self.address = address
        self.web3 = Web3(provider)
        # Verify successfully connected
        if not self.web3.isConnected():
            raise ConnectionError("Could not connect to the network")
        # Verify if provided address is a valid eth address
        if not self.web3.isChecksumAddress(self.address):
            raise InvalidAddress(
                f"Provided {self.address} address is not valid. Please provide valid"
                " wallet address."
            )
        self.web3.eth.account.privateKeyToAccount(private_key)

    def send_token(
        self, token_address: Address, to_address: Address, amount: int
    ) -> TxReceipt:
        """Send token.

        Args:
            token_address (Address): Token address
            to_address (Address): Address of a reciever
            amount (int): amount of tokens to send (in Wei)
        """

        contract = self.web3.eth.contract(address=token_address, abi=ABI)
        tx_hash = contract.functions.transfer(to_address, amount).estimate_gas(
            {"from": self.address}
        )
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def get_token_balance(self, token_address: Address) -> str:
        """Get balance on ERC20 token

        Args:
            token_address (Address): Address of a token

        Returns:
            str: balance in Wei
        """
        checksumAddress = self.web3.toChecksumAddress(token_address)
        contract = self.web3.eth.contract(address=checksumAddress, abi=ABI)
        balance = contract.functions.balanceOf(self.address).call()
        return balance


__all__ = ["Wallet"]
