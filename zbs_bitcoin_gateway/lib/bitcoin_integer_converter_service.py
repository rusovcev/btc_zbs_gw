"""
BitcoinIntegerConverterService
"""

from numbers import Number

import zbs_gateway as gw
from decimal import Decimal


class BitcoinIntegerConverterService(gw.IntegerConverterService):
    """
    Implementation of an IntegerConverterService.
    Converts the Decimal values provided by the bitcoinrpc package into integers that can be processed
    by the Gateway.
    """

    def __init__(self, btc_factor: int, btc_round_precision: int) -> None:
        self._btc_factor = btc_factor
        self._btc_round_precision = btc_round_precision

    def convert_amount_to_int(self, amount: Decimal) -> int:
        return gw.convert_to_int(amount, self._btc_factor)

    def revert_amount_conversion(self, amount: int) -> Number:
        return gw.convert_to_decimal(amount, self._btc_factor, self._btc_round_precision)
