"""
AssetTransactionServiceImpl
"""

from typing import Optional

from zbs_gateway.common import ZbsPyError, Injectable, ZBS_ASSET_ID, GATEWAY_ZBSPY_ADDRESS
from zbs_gateway.model import TransactionReceiver, TransactionAttempt, Transaction
from .transaction_service import TransactionService
# import pywaves as pw  # type: ignore
import zbspy as pw


@Injectable(deps=[ZBS_ASSET_ID, GATEWAY_ZBSPY_ADDRESS])
class AssetTransactionServiceImpl(TransactionService):
    """
    Implements a TransactionService that is capable of processing an TransactionAttempt instance
    with a 'waves' currency.
    """

    def __init__(self, zbs_asset_id: str, gateway_zbspy_address: pw.Address) -> None:
        self._z_coin = pw.Asset(zbs_asset_id)
        self._gateway_zbspy_address = gateway_zbspy_address

    def send_coin(self, attempt: TransactionAttempt, secret: Optional[str]) -> Transaction:
        if attempt.sender != self._gateway_zbspy_address.address:
            raise ZbsPyError('Missing secret for sender ' + attempt.sender)

        transaction = self._gateway_zbspy_address.sendAsset(
            recipient=pw.Address(attempt.receivers[0].address),
            asset=self._z_coin,
            amount=attempt.receivers[0].amount,
            txFee=attempt.fee)

        if transaction is None:
            raise ZbsPyError("Encountered an unknown exception while trying to perform waves transaction.")

        return Transaction(
            tx=transaction['id'],
            receivers=[TransactionReceiver(transaction['recipient'], attempt.receivers[0].amount)])
