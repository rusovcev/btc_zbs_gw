"""
WavesAddressValidationService
"""

from doc_inherit import class_doc_inherit

from zbs_gateway.common import Injectable
from .address_validation_service import AddressValidationService

# import pywaves
import zbspy # as pywaves


@Injectable()
@class_doc_inherit
class ZbsAddressValidationService(AddressValidationService):
    """inherit"""

    def validate_address(self, address: str) -> bool:
        try:
            zbspy.Address(address=address)
            return True
        except ValueError:
            return False
