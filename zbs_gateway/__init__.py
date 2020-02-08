"""
Waves Gateway Library
========================

Contains tools to create a new Waves Cryptocurrency Gateway.
It is recommended to call gevent.monkey.patch_all() at the very beginning of the application
as this library uses gevent for non-blocking io.
"""

import gevent.monkey
gevent.monkey.patch_all()

import gevent.hub
gevent.hub.Hub.NOT_ERROR = (Exception, )

from zbs_gateway.factory import CoinAddressFactory
from zbs_gateway.model import KeyPair, \
    TransactionAttemptReceiver, \
    TransactionAttempt, Transaction, TransactionReceiver, TransactionSender, PollingDelayConfig, GatewayConfigFile
from .gateway import Gateway
from zbs_gateway.service import ChainQueryService, TransactionService, IntegerConverterService, \
    FeeService, ConstantFeeServiceImpl, AddressValidationService, COIN_INTEGER_CONVERTER_SERVICE, COIN_TRANSACTION_SERVICE, COIN_CHAIN_QUERY_SERVICE, COIN_ADDRESS_VALIDATION_SERVICE, GatewayConfigParser, GatewayApplicationService
from zbs_gateway.storage import WalletStorage, MapStorage, KeyValueStorage
from zbs_gateway.common import convert_to_int, convert_to_decimal, ProxyGuard, InvalidTransactionIdentifier, InjectionToken, Injectable, Factory, INJECTOR, Injector, InjectorError, Token, COIN_NODE, CUSTOM_CURRENCY_NAME, ZBS_ASSET_ID, ProxyFactory

from typing import NewType

CoinAddress = NewType('CoinAddress', str)
ZbsAddress = NewType('ZbsAddress', str)

ZbsAddressSecret = NewType('ZbsAddressSecret', KeyPair)
CoinAddressSecret = NewType('CoinAddressSecret', KeyPair)

CoinTransactionIdentifier = NewType('CoinTransactionIdentifier', str)
ZbsTransactionIdentifier = NewType('ZbsTransactionIdentifier', str)

CoinBlockHeight = NewType('CoinBlockHeight', int)
ZbsBlockHeight = NewType('ZbsBlockHeight', int)

ZbsTransaction = NewType('ZbsTransaction', Transaction)
CoinTransaction = NewType('CoinTransaction', Transaction)

CoinAmount = NewType('CoinAmount', int)
