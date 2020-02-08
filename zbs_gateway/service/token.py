"""
List of tokens that are provided by the service module.
"""

from .chain_query_service import ChainQueryService
from zbs_gateway.common import InjectionToken
from .address_validation_service import AddressValidationService
from .transaction_service import TransactionService
from .integer_converter_service import IntegerConverterService
from .transaction_polling_service import TransactionPollingService

COIN_ADDRESS_VALIDATION_SERVICE = InjectionToken('COIN_ADDRESS_VALIDATION_SERVICE', AddressValidationService)
COIN_CHAIN_QUERY_SERVICE = InjectionToken('COIN_CHAIN_QUERY_SERVICE', ChainQueryService)
ZBS_CHAIN_QUERY_SERVICE = InjectionToken('ZBS_CHAIN_QUERY_SERVICE', ChainQueryService)
COIN_TRANSACTION_SERVICE = InjectionToken('COIN_TRANSACTION_SERVICE', TransactionService)
COIN_INTEGER_CONVERTER_SERVICE = InjectionToken('COIN_INTEGER_CONVERTER_SERVICE', IntegerConverterService)
ASSET_INTEGER_CONVERTER_SERVICE = InjectionToken('ASSET_INTEGER_CONVERTER_SERVICE', IntegerConverterService)
COIN_TRANSACTION_SERVICE_CONVERTER_PROXY = InjectionToken('COIN_TRANSACTION_SERVICE_CONVERTER_PROXY',
                                                          TransactionService)
ZBS_TRANSACTION_SERVICE_CONVERTER_PROXY = InjectionToken('ZBS_TRANSACTION_SERVICE_CONVERTER_PROXY',
                                                           TransactionService)
COIN_TRANSACTION_POLLING_SERVICE = InjectionToken('COIN_TRANSACTION_POLLING_SERVICE', TransactionPollingService)
ZBS_TRANSACTION_POLLING_SERVICE = InjectionToken('ZBS_TRANSACTION_POLLING_SERVICE', TransactionPollingService)
