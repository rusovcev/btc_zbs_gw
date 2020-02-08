"""
PublicConfiguration
"""

from typing import Optional


class PublicConfiguration:
    """
    Part of the configuration that is allowed to be available to the public,
    for example via ReST.
    """

    CUSTOM_CURRENCY_NAME_DICT_KEY = 'custom_currency_name'
    GATEWAY_ZBS_ADDRESS_DICT_KEY = 'gateway_zbs_address'
    GATEWAY_COIN_HOLDER_DICT_KEY = 'gateway_coin_holder'
    ZBS_NODE_DICT_KEY = 'zbs_node'
    ZBS_ASSET_ID = 'zbs_asset_id'
    COIN_TRANSACTION_WEB_LINK = 'coin_transaction_web_link'
    ZBS_TRANSACTION_WEB_LINK = 'zbs_transaction_web_link'
    COIN_ADDRESS_WEB_LINK = 'coin_address_web_link'
    ZBS_ADDRESS_WEB_LINK = 'zbs_address_web_link'
    WEB_PRIMARY_COLOR = 'web_primary_color'

    def __init__(self,
                 custom_currency_name: str,
                 gateway_zbs_address: str,
                 gateway_coin_address: str,
                 zbs_node: str,
                 zbs_asset_id: str,
                 zbs_transaction_web_link: str,
                 zbs_address_web_link: str,
                 coin_transaction_web_link: Optional[str] = None,
                 coin_address_web_link: Optional[str] = None,
                 web_primary_color: Optional[str] = None) -> None:
        self._custom_currency_name = custom_currency_name
        self._gateway_zbs_address = gateway_zbs_address
        self._gateway_coin_holder = gateway_coin_address
        self._zbs_node = zbs_node
        self._zbs_asset_id = zbs_asset_id
        self._coin_transaction_web_link = coin_transaction_web_link
        self._zbs_transaction_web_link = zbs_transaction_web_link
        self._zbs_address_web_link = zbs_address_web_link
        self._coin_address_web_link = coin_address_web_link
        self._web_primary_color = web_primary_color

    @property
    def custom_currency_name(self) -> str:
        return self._custom_currency_name

    @property
    def gateway_zbs_address(self) -> str:
        return self._gateway_zbs_address

    @property
    def gateway_coin_holder(self) -> str:
        return self._gateway_coin_holder

    @property
    def zbs_node(self) -> str:
        return self._zbs_node

    @property
    def zbs_asset_id(self) -> str:
        return self._zbs_asset_id

    @property
    def zbs_transaction_web_link(self) -> str:
        return self._zbs_transaction_web_link

    @property
    def coin_address_web_link(self) -> Optional[str]:
        return self._coin_address_web_link

    @property
    def coin_transaction_web_link(self) -> Optional[str]:
        return self._coin_transaction_web_link

    @property
    def zbs_address_web_link(self) -> str:
        return self._zbs_address_web_link

    @property
    def web_primary_color(self) -> str:
        return self._web_primary_color
