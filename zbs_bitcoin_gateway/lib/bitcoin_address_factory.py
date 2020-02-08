"""
BitcoinAddressFactory
"""

import zbs_gateway as gw
from bitcoinrpc.authproxy import AuthServiceProxy


class BitcoinAddressFactory(gw.CoinAddressFactory):
    """
    Implements an AddressFactory using the getnewaddress function provided by the Bitcoin client.
    """

    def __init__(self, btc_proxy: AuthServiceProxy) -> None:
        self._access = btc_proxy

    def create_address(self) -> gw.CoinAddress:

        return self._access.getnewaddress()
