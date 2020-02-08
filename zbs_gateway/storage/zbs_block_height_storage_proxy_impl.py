"""
ZbsBlockHeightStorageProxyImpl
"""

from typing import Optional
from doc_inherit import method_doc_inherit  # type: ignore

from zbs_gateway.common import Injectable
from zbs_gateway.storage.key_value_storage import KeyValueStorage
from zbs_gateway.storage.block_height_storage_proxy import BlockHeightStorageProxy


@Injectable(deps=[KeyValueStorage])
class ZbsBlockHeightStorageProxyImpl(BlockHeightStorageProxy):
    """
    Forwards requests for the block height to the KeyValueStorage.
    """

    def __init__(self, key_value_storage: KeyValueStorage) -> None:
        self._key_value_storage = key_value_storage

    @method_doc_inherit
    def set_last_checked_block_height(self, block_height: int) -> None:
        return self._key_value_storage.set_last_checked_zbs_block_height(block_height)

    @method_doc_inherit
    def get_last_checked_block_height(self) -> Optional[int]:
        return self._key_value_storage.get_last_checked_zbs_block_height()
