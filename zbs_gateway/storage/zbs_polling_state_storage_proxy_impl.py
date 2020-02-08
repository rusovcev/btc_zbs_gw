"""
ZbsPollingStateStorageProxyImpl
"""

from zbs_gateway.common import Injectable

from zbs_gateway.model import PollingState
from .polling_state_storage_proxy import PollingStateStorageProxy
from .key_value_storage import KeyValueStorage


@Injectable(deps=[KeyValueStorage])
class ZbsPollingStateStorageProxyImpl(PollingStateStorageProxy):
    """Forwards polling_state requests to the waves methods of KeyValueStorage."""

    def __init__(self, key_value_storage: KeyValueStorage) -> None:
        self._storage = key_value_storage

    def set_polling_state(self, state: PollingState) -> None:
        self._storage.set_zbs_polling_state(state)

    def get_polling_state(self) -> PollingState:
        return self._storage.get_zbs_polling_state()
