"""
BitcoinGateway
"""

import logging
from logging.handlers import RotatingFileHandler
from typing import List

import bitcoinrpc.authproxy as authproxy
import pymongo
import zbs_gateway as wg

import zbs_bitcoin_gateway.lib as lib


class BitcoinGateway(object):
    """
    Implements an BTC Gateway.
    """

    DEFAULT_ZBS_CHAIN = "testnet"
    DEFAULT_BTC_FACTOR = pow(10, 8)
    DEFAULT_BTC_ROUND_PRECISION = 8
    # DEFAULT_TRANSACTION_WEB_LINK = "https://live.blockcypher.com/ltc/tx/{{tx}}"
    DEFAULT_TRANSACTION_WEB_LINK = "https://live.blockcypher.com/btc-testnet/tx/{{tx}}"
    # DEFAULT_ADDRESS_WEB_LINK = "https://live.blockcypher.com/ltc/tx/{{tx}}"
    DEFAULT_ADDRESS_WEB_LINK = "https://live.blockcypher.com/btc-testnet/address/{{address}}"
    DEFAULT_MONGO_DATABASE = "btc-gateway"
    # WEB_CURRENCY_NAME = "Litecoin"
    WEB_CURRENCY_NAME = "tBTC"
    # WAVES_ASSET_ID = "HtuMVfunYhNpsqhFotXuwXvrC9wt6UD6ENdpQEQxtGAv"
    # WAVES_ASSET_ID = "EWXnEHoqLgevZVuwTTjCeiH21C1aL87AfxnzGAhHrUni"
    ZBS_ASSET_ID = "En95hR33MkjcecoNt8hhLdJCSMgpbzSkuadZBSvyRRHt" # zBTC
    DEFAULT_PORT = 5000
    DEFAULT_HOST = 'localhost'

    def __init__(self,
                 config: wg.GatewayConfigFile,
                 btc_round_precision: int = DEFAULT_BTC_ROUND_PRECISION,
                 btc_factor: int = DEFAULT_BTC_FACTOR,
                 transaction_web_link: str = DEFAULT_TRANSACTION_WEB_LINK,
                 address_web_link: str = DEFAULT_ADDRESS_WEB_LINK) -> None:
        btc_proxy = wg.ProxyGuard(authproxy.AuthServiceProxy(config.coin_node), max_parallel_access=1)
        bitcoin_address_factory = lib.BitcoinAddressFactory(btc_proxy)
        bitcoin_chain_query_service = lib.BitcoinChainQueryService(btc_proxy)
        bitcoin_transaction_service = lib.BitcoinTransactionService(btc_proxy, bitcoin_chain_query_service)
        bitcoin_integer_converter_service = lib.BitcoinIntegerConverterService(btc_factor, btc_round_precision)
        bitcoin_address_validation_service = lib.BitcoinAddressValidationService(btc_proxy)
        mongo_client = pymongo.MongoClient(host=config.mongo_host, port=config.mongo_port)
        fee_service = wg.ConstantFeeServiceImpl(config.gateway_fee, config.coin_fee)

        logging_handlers = self._init_logging_handlers(config.environment)

        self._gateway = wg.Gateway(
            coin_address_factory=bitcoin_address_factory,
            coin_chain_query_service=bitcoin_chain_query_service,
            coin_transaction_service=bitcoin_transaction_service,
            gateway_zbs_address_secret=config.gateway_zbs_address_secret,
            gateway_coin_address_secret=config.gateway_coin_address_secret,
            mongo_database=mongo_client.get_database(config.mongo_database),
            managed_loggers=["BitcoinRPC"],
            logging_handlers=logging_handlers,
            custom_currency_name=BitcoinGateway.WEB_CURRENCY_NAME,
            coin_integer_converter_service=bitcoin_integer_converter_service,
            asset_integer_converter_service=wg.IntegerConverterService(),
            zbs_chain=config.zbs_chain,
            zbs_asset_id=BitcoinGateway.ZBS_ASSET_ID,
            zbs_node=config.zbs_node,
            gateway_owner_address=config.gateway_owner_address,
            fee_service=fee_service,
            only_one_transaction_receiver=False,
            coin_transaction_web_link=transaction_web_link,
            coin_address_web_link=address_web_link,
            host=config.gateway_host,
            port=config.gateway_port,
            coin_address_validation_service=bitcoin_address_validation_service,
            coin_last_block_distance=5)
            # coin_last_block_distance=1)

    def _init_logging_handlers(self, environment: str) -> List[logging.Handler]:
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s {%(name)s} - %(message)s")
        logging_handlers = []  # type: List[logging.Handler]

        if environment == "prod":
            file_handler = RotatingFileHandler("btc-gateway.log", maxBytes=10485760, backupCount=20, encoding='utf8')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            logging_handlers.append(file_handler)

            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.WARN)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)

        elif environment == "debug":
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatter)
            logging_handlers.append(stream_handler)

        elif environment == "test":
            pass

        else:
            raise Exception('Unknown environment ' + environment + '. Use prod or debug')

        return logging_handlers

    def run(self):
        self._gateway.run()

    def set_log_level(self, level):
        self._gateway.set_log_level(level)

    @staticmethod
    def from_config_file(file_content: str):
        parser = wg.INJECTOR.get(wg.GatewayConfigParser)
        parsed_config = parser.parse_config_file_content(file_content)
        return BitcoinGateway(config=parsed_config)
