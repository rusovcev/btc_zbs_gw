"""
ConstantFeeServiceImpl
"""

from typing import Optional, Union

from decimal import Decimal

from .fee_service import FeeService


class ConstantFeeServiceImpl(FeeService):
    """
    Implements a FeeService that uses constant values.
    """

    def __init__(self, gateway_fee: Union[int, Decimal], coin_fee: Union[int, Decimal],
                 zbs_fee: Optional[int] = None) -> None:
        self._gateway_fee = gateway_fee
        self._coin_fee = coin_fee
        self._zbs_fee = zbs_fee

    def get_gateway_fee(self) -> Union[int, Decimal]:
        return self._gateway_fee

    def get_coin_fee(self) -> Union[int, Decimal]:
        return self._coin_fee

    def get_zbs_fee(self) -> int:
        if self._zbs_fee is not None:
            return self._zbs_fee
        else:
            return super().get_zbs_fee()
