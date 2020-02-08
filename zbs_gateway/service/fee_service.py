"""
FeeService
"""

from abc import ABC, abstractmethod
from typing import Union

# import pywaves  # type: ignore
import zbspy # as pywaves
from decimal import Decimal


class FeeService(ABC):
    """
    Defines the fee values, the Gateway requires. The waves_fee may also be overwritten of required.
    """

    @abstractmethod
    def get_coin_fee(self) -> Union[int, Decimal]:
        pass

    @abstractmethod
    def get_gateway_fee(self) -> Union[int, Decimal]:
        pass

    def get_zbs_fee(self) -> int:
        return zbspy.DEFAULT_TX_FEE
