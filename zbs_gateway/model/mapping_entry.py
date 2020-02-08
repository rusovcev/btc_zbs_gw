"""
MappingEntry
"""


class MappingEntry(object):
    """
    Defines what will be saved in the MapStorage.
    A MappingEntry represents a connection between a custom currency address and a Waves address.
    """

    DICT_COIN_KEY = 'coin'
    DICT_ZBS_KEY = 'waves'

    def __init__(self, zbs_address: str, coin_address: str) -> None:
        self._zbs_address = zbs_address
        self._coin_address = coin_address

    @property
    def zbs_address(self) -> str:
        return self._zbs_address

    @property
    def coin_address(self) -> str:
        return self._coin_address

    def __str__(self):
        return "Coin(" + str(self._coin_address) + ")" + " -> " + "Zbs(" + str(self._zbs_address) + ")"

    def __eq__(self, other):
        return self.zbs_address == other.zbs_address and self.coin_address == other.coin_address
