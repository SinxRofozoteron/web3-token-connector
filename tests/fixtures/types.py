from typing import TypedDict

from eth_typing.evm import ChecksumAddress, HexStr


class TEthAccount(TypedDict):

    address: ChecksumAddress
    private_key: HexStr


__all__ = ["TEthAccount"]
