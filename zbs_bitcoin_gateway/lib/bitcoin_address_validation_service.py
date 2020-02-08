"""
BitcoinAddressValidationService
"""

import zbs_gateway as wg
from bitcoinrpc.authproxy import AuthServiceProxy


class BitcoinAddressValidationService(wg.AddressValidationService):
    """
    Validates an Bitcoin address by using an RPC service.
    """

    def __init__(self, btc_proxy: AuthServiceProxy) -> None:
        self._btc_proxy = btc_proxy

    def validate_address(self, address: str) -> bool:
        validation_result = self._btc_proxy.validateaddress(address)
        return validation_result['isvalid']
