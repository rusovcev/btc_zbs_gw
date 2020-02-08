"""
GatewayControllerImpl
"""

from doc_inherit import method_doc_inherit, class_doc_inherit  # type: ignore

from logging import Logger
from typing import Optional, List

from zbs_gateway.common import ZbsAddressInvalidError, InvalidTransactionIdentifier, Injectable, \
    COIN_CHAIN_QUERY_SERVICE_CONVERTER_PROXY, ZBS_CHAIN_QUERY_SERVICE_CONVERTER_PROXY
from zbs_gateway.factory.coin_address_factory import CoinAddressFactory
from zbs_gateway.model import MappingEntry, KeyPair, AttemptListTrigger, \
    TransactionAttemptList, AttemptListQuery
from zbs_gateway.service import ChainQueryService, TransactionConsumer, \
    AddressValidationService, ZbsAddressValidationService, ZbsTransactionConsumerImpl, \
    CoinTransactionConsumerImpl
from zbs_gateway.storage import TransactionAttemptListStorage
from zbs_gateway.storage.map_storage import MapStorage
from zbs_gateway.storage.wallet_storage import WalletStorage
from .gateway_controller import GatewayController


@Injectable(
    provides=GatewayController,
    deps=[
        CoinAddressFactory, Logger, MapStorage, WalletStorage, TransactionAttemptListStorage,
        ZbsAddressValidationService, ZBS_CHAIN_QUERY_SERVICE_CONVERTER_PROXY,
        COIN_CHAIN_QUERY_SERVICE_CONVERTER_PROXY, CoinTransactionConsumerImpl, ZbsTransactionConsumerImpl
    ])
@class_doc_inherit
class GatewayControllerImpl(GatewayController):
    """inherit"""

    def __init__(self, coin_address_factory: CoinAddressFactory, logger: Logger, map_storage: MapStorage,
                 wallet_storage: WalletStorage, attempt_list_storage: TransactionAttemptListStorage,
                 zbs_address_validation_service: AddressValidationService,
                 zbs_chain_query_service: ChainQueryService, coin_chain_query_service: ChainQueryService,
                 coin_transaction_consumer: TransactionConsumer,
                 zbs_transaction_consumer: TransactionConsumer) -> None:
        self._coin_address_factory = coin_address_factory
        self._map_storage = map_storage
        self._wallet_storage = wallet_storage
        self._logger = logger.getChild('GatewayControllerImpl')
        self._attempt_list_storage = attempt_list_storage
        self._zbs_address_validation_service = zbs_address_validation_service
        self._zbs_chain_query_service = zbs_chain_query_service
        self._coin_chain_query_service = coin_chain_query_service
        self._coin_transaction_consumer = coin_transaction_consumer
        self._zbs_transaction_consumer = zbs_transaction_consumer

    @method_doc_inherit
    def check_zbs_transaction(self, tx: str) -> None:
        transaction = self._zbs_chain_query_service.get_transaction_by_tx(tx)

        if transaction is None:
            raise InvalidTransactionIdentifier()

        if self._zbs_transaction_consumer.filter_transaction(transaction):
            self._zbs_transaction_consumer.handle_transaction(transaction)

    @method_doc_inherit
    def check_coin_transaction(self, tx: str) -> None:
        transaction = self._coin_chain_query_service.get_transaction_by_tx(tx)

        if transaction is None:
            raise InvalidTransactionIdentifier()

        if self._coin_transaction_consumer.filter_transaction(transaction):
            self._coin_transaction_consumer.handle_transaction(transaction)

    @method_doc_inherit
    def validate_zbs_address(self, address: str) -> bool:
        """inherit"""
        return self._zbs_address_validation_service.validate_address(address)

    @method_doc_inherit
    def create_address(self, zbs_address: str) -> str:
        """inherit"""
        self._logger.debug("Client requested coin address for ZBS address '%s'", zbs_address)

        if not self._zbs_address_validation_service.validate_address(zbs_address):
            raise ZbsAddressInvalidError()

        if self._map_storage.zbs_address_exists(zbs_address):
            coin_address = self._map_storage.get_coin_address_by_zbs_address(zbs_address)
            self._logger.debug("Found associated coin_address '%s'", coin_address)
            return coin_address
        else:
            create_address_result = self._coin_address_factory.create_address()

            if isinstance(create_address_result, str):
                mapping = MappingEntry(zbs_address, create_address_result)
                self._map_storage.safely_save_mapping(mapping)
                self._logger.info("Created new mapping '%s'", str(mapping))
                return create_address_result
            elif isinstance(create_address_result, KeyPair):
                mapping = MappingEntry(zbs_address, create_address_result.public)
                self._wallet_storage.safely_save_address_secret(create_address_result)
                self._map_storage.safely_save_mapping(mapping)
                self._logger.info("Created new mapping '%s'", str(mapping))

                return create_address_result.public
            else:
                raise TypeError('Result of create_address is neither a CoinAddress nor a CoinAddressSecret')

    @method_doc_inherit
    def get_attempt_list_by_id(self, attempt_list_id: str) -> Optional[TransactionAttemptList]:
        return self._attempt_list_storage.find_by_attempt_list_id(attempt_list_id)

    @method_doc_inherit
    def query_attempt_lists(self, query: AttemptListQuery) -> List[TransactionAttemptList]:
        return self._attempt_list_storage.query_attempt_lists(query)

    @method_doc_inherit
    def get_attempt_list_by_trigger(self, trigger: AttemptListTrigger) -> Optional[TransactionAttemptList]:
        return self._attempt_list_storage.find_by_trigger(trigger)
