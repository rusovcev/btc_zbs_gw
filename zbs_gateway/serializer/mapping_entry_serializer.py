"""
MappingEntrySerializer
"""
from zbs_gateway.common import Injectable
from zbs_gateway.model import MappingEntry


@Injectable()
class MappingEntrySerializer(object):
    """
    Defines how a MappingEntry can be serialized and deserialized.
    """

    # noinspection PyMethodMayBeStatic
    def as_dict(self, entry: MappingEntry) -> dict:
        """
        Converts a mapping entry into a dictionary containing all attributes.
        """
        res = dict()

        res[MappingEntry.DICT_ZBS_KEY] = entry.zbs_address
        res[MappingEntry.DICT_COIN_KEY] = entry.coin_address

        return res
