"""
SecretService
"""

# import pywaves  # type: ignore
import zbspy # as pywaves

from zbs_gateway.common import Injectable, GATEWAY_COIN_ADDRESS_SECRET, GATEWAY_ZBSPY_ADDRESS
from zbs_gateway.storage import WalletStorage
from zbs_gateway.model import KeyPair


@Injectable(deps=[WalletStorage, GATEWAY_COIN_ADDRESS_SECRET, GATEWAY_ZBSPY_ADDRESS])
class SecretService(object):
    """
    Forwards to the specific secret if any.
    Can be used to query any secret that the Gateway stores.
    """

    def __init__(self, wallet_storage: WalletStorage, gateway_coin_address_secret: KeyPair,
                 gateway_zbspy_address: zbspy.Address) -> None:
        self._wallet_storage = wallet_storage
        self._coin_gateway_address_secret = gateway_coin_address_secret
        self._gateway_zbspy_address = gateway_zbspy_address

    def get_secret_by_address(self, currency: str, address: str):
        if currency == "zbs" and self._gateway_zbspy_address.address == address:
            return self._gateway_zbspy_address.privateKey
        elif currency == "coin":
            if self._coin_gateway_address_secret.public == address:
                return self._coin_gateway_address_secret.secret
            else:
                key_pair = self._wallet_storage.get_secret_by_public_address(address)
                if key_pair is not None:
                    return key_pair.secret
        return None
