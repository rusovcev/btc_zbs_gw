"""
PublicConfigurationSerializer
"""
from zbs_gateway.common import Injectable
from zbs_gateway.model import PublicConfiguration


@Injectable()
class PublicConfigurationSerializer(object):
    """
    Defines the conversion of a PublicConfiguration instance into a dict object.
    The resulting object may be delivered to the Web Application.
    """

    def as_dict(self, value: PublicConfiguration) -> dict:
        res = dict()

        res[PublicConfiguration.CUSTOM_CURRENCY_NAME_DICT_KEY] = value.custom_currency_name
        res[PublicConfiguration.GATEWAY_ZBS_ADDRESS_DICT_KEY] = value.gateway_zbs_address
        res[PublicConfiguration.GATEWAY_COIN_HOLDER_DICT_KEY] = value.gateway_coin_holder
        res[PublicConfiguration.ZBS_NODE_DICT_KEY] = value.zbs_node
        res[PublicConfiguration.ZBS_ASSET_ID] = value.zbs_asset_id
        res[PublicConfiguration.WEB_PRIMARY_COLOR] = value.web_primary_color

        if value.coin_transaction_web_link is not None:
            res[PublicConfiguration.COIN_TRANSACTION_WEB_LINK] = value.coin_transaction_web_link

        if value.coin_address_web_link is not None:
            res[PublicConfiguration.COIN_ADDRESS_WEB_LINK] = value.coin_address_web_link

        res[PublicConfiguration.ZBS_ADDRESS_WEB_LINK] = value.zbs_address_web_link
        res[PublicConfiguration.ZBS_TRANSACTION_WEB_LINK] = value.zbs_transaction_web_link

        return res
