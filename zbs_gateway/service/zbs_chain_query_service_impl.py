"""
ZbsChainQueryServiceImpl
"""
from zbs_gateway.common import map_array, filter_array, Injectable, ZBS_NODE, ZBS_ASSET_ID, ZbsNodeException
from zbs_gateway.model import TransactionReceiver, Transaction, TransactionSender
from typing import List, Optional

import gevent.pool
from .chain_query_service import ChainQueryService
from doc_inherit import method_doc_inherit  # type: ignore
import requests
import simplejson as json  # type: ignore
import base58  # type: ignore
from .token import ZBS_CHAIN_QUERY_SERVICE


@Injectable(provides=ZBS_CHAIN_QUERY_SERVICE, deps=[ZBS_NODE, ZBS_ASSET_ID])
class ZbsChainQueryServiceImpl(ChainQueryService):
    """
    Implements the ChainQueryService for the ZBS Blockchain.
    It requires a zbs_node that is used for the requests.
    """

    def __init__(self, zbs_node: str, asset_id: str) -> None:
        self._zbs_node = zbs_node
        self._asset_id = asset_id

    def _get_response_from_node(self, path):
        response = requests.get(self._zbs_node + path)

        if not response.ok:
            raise ZbsNodeException(response.url, response.status_code, response.text)
        else:
            return json.loads(response.text)

    def _convert_node_response_to_transaction(self, res: dict) -> Optional[Transaction]:
        if 'assetId' not in res or res['assetId'] != self._asset_id:
            return None

        if res['type'] != 4:
            return None

        try:
            address = res['recipient'].split(':')[1]
        except IndexError:
            address = res['recipient']
        try:
            sender = res['sender'].split(':')[1]
        except IndexError:
            sender = res['sender']

        return Transaction(
            tx=res['id'],
            receivers=[TransactionReceiver(address=address, amount=res['amount'])],
            senders=[TransactionSender(address=sender)])

    @method_doc_inherit
    def get_transactions_of_block_at_height(self, height: int) -> List[Transaction]:
        transactions = self._get_response_from_node('/blocks/at/' + str(height))['transactions']
        zbs_transactions = map_array(self._convert_node_response_to_transaction, transactions)
        return filter_array(lambda x: x is not None, zbs_transactions)

    @method_doc_inherit
    def get_height_of_highest_block(self) -> int:
        return self._get_response_from_node('/blocks/height')['height']

    def get_coin_receiver_address_from_transaction(self, transaction: str) -> str:
        """
        Returns the custom currency address that shall be benefited by this transaction
        """
        attachment = self._get_response_from_node('/transactions/info/' + transaction)['attachment']

        return base58.b58decode(attachment).decode("utf-8")

    @method_doc_inherit
    def get_transaction_by_tx(self, tx: str) -> Optional[Transaction]:
        res = self._get_response_from_node('/transactions/info/' + tx)

        if 'status' in res and res['status'] == 'error':
            return None

        return self._convert_node_response_to_transaction(res)
