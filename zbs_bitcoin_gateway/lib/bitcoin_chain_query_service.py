"""
BitcoinChainQueryService
"""

import zbs_gateway as gw
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from typing import List, Optional
import gevent.pool as pool

from decimal import Decimal

from zbs_gateway import Transaction

from .util import sum_unspents


class BitcoinChainQueryService(gw.ChainQueryService):
    """
    Implementation of an ChainQueryService on the Litecoin Blockchain.
    """

    def get_transaction_by_tx(self, tx: str) -> Optional[Transaction]:
        try:
            return self.get_transaction(tx)
        except JSONRPCException:
            raise gw.InvalidTransactionIdentifier()

    def __init__(self, btc_proxy: AuthServiceProxy) -> None:
        self._btc_proxy = btc_proxy

    def _extract_receivers(self, transaction: dict) -> List[gw.TransactionReceiver]:
        """Extracts the receivers of an unparsed LTC transaction."""
        results = list()  # type: List[gw.TransactionReceiver]

        for vout in transaction['vout']:
            if 'addresses' not in vout['scriptPubKey']:
                # print("no ADDRESSES in VOUT[SCRIPTPUBKEY]?")
                continue

            for address in vout['scriptPubKey']['addresses']:
                btc_transaction_receiver = gw.TransactionReceiver(address=address, amount=vout['value'])
                results.append(btc_transaction_receiver)

        return results

    def _filter_sender_duplicates(self, senders: List[gw.TransactionSender]) -> List[gw.TransactionSender]:
        results = list()  # type: List[gw.TransactionSender]

        for sender in senders:
            if sender not in results:
                results.append(sender)

        return results

    def _resolve_senders(self, transaction: dict) -> List[gw.TransactionSender]:
        """Extracts the senders of an unparsed BTC transaction"""

        if 'vin' not in transaction:
            # print("no VIN in TRANSACTION?")
            return list()

        results = list()  # type: List[gw.TransactionSender]

        for vin in transaction['vin']:

            if ('txid' not in vin) or ('vout' not in vin):
                # print("no VOUT or TXID in VIN?")
                continue

            vin_transaction_raw = self._btc_proxy.getrawtransaction(vin['txid'])
            # print(vin["txid"])
            vin_transaction = self._btc_proxy.decoderawtransaction(vin_transaction_raw)

            try:
                if 'addresses' not in vin_transaction['vout'][vin['vout']]['scriptPubKey']:
                    continue
            except Exception as ex:
                print(ex.args)
                continue
            finally:
                pass

            for address in vin_transaction['vout'][vin['vout']]['scriptPubKey']['addresses']:
                btc_transaction_sender = gw.TransactionSender(address=address)
                results.append(btc_transaction_sender)

        return self._filter_sender_duplicates(results)

    def get_transaction(self, tx: str) -> gw.Transaction:
        raw_transaction = self._btc_proxy.getrawtransaction(tx)
        transaction = self._btc_proxy.decoderawtransaction(raw_transaction)

        transaction_receivers = self._extract_receivers(transaction)
        transaction_sender = self._resolve_senders(transaction)

        # if transaction_sender and transaction_receivers:
        #     # print("-"*40)
        #     # print("tx_sender(s):")
        #     for sender in transaction_sender:
        #         # if sender._address == "2MtGWRsjDUyhTxUHjH3nw4Z2b8NEZStCRCc" or sender._address == "2NA68kNWVuZo7LpjHZ5QRegNDPyEjhfuAvJ" or sender._address == "2MwFvkpBYKVFsqoGJdvAs71hg2t9NpccEdw":
        #         print(" -", sender.address)
        #     # print("tx_receiver(s):")
        #     for receiver in transaction_receivers:
        #         if receiver._address == "2MtGWRsjDUyhTxUHjH3nw4Z2b8NEZStCRCc": # or receiver._address == "2NA68kNWVuZo7LpjHZ5QRegNDPyEjhfuAvJ" or receiver._address == "2MwFvkpBYKVFsqoGJdvAs71hg2t9NpccEdw":
        #             print(" +", receiver._address, receiver.amount)

        return gw.Transaction(tx, transaction_receivers, transaction_sender)

    def get_transactions_of_block_at_height(self, height: gw.CoinBlockHeight) -> List[gw.Transaction]:
        block_hash = self._btc_proxy.getblockhash(height)
        block = self._btc_proxy.getblock(block_hash)

        get_transaction_tasks = pool.Pool()  # litecoin server does not accept more than one parallel connection

        return [a for a in get_transaction_tasks.map(self.get_transaction, block['tx'])]

    def get_amount_of_transaction(self, transaction: str) -> Decimal:
        transaction = self._btc_proxy.gettransaction(transaction)
        # print("--------- AMOUNT of TRANSACTION -------------------")
        # print(transaction["amount"])
        return transaction['amount']  # type: ignore

    def get_height_of_highest_block(self) -> gw.CoinBlockHeight:
        info = self._btc_proxy.getblockchaininfo()
        # conncount = self._ltc_proxy.getconnectioncount()
        if info:
        #     print("-------------- BLOCK height ------------------")
            # print("+++ block height:", info["blocks"])
            pass
        # #     print("conn_count:", conncount)
        # #     print("----------------------------------------------")
        return info['blocks']
