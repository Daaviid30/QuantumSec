"""HQC-3 key encapsulation executed by liboqs."""

from dataclasses import dataclass
from functools import cache
from typing import ClassVar, Final

from pqc.backends.oqs_kem_backend import OQSKEMBackend
from pqc.errors import BackendOperationError
from pqc.kem._oqs_provider import OQSKEMProvider
from pqc.kem.base import KEMMetadata

HQC_3_ALGORITHM: Final = "HQC-3"


@cache
def hqc_3_metadata() -> KEMMetadata:
    """Return backend-derived HQC-3 metadata."""

    details = OQSKEMBackend().details(HQC_3_ALGORITHM)
    if details.name != HQC_3_ALGORITHM or details.claimed_nist_level != 3:
        raise BackendOperationError("liboqs returned inconsistent HQC-3 metadata.")
    return KEMMetadata(
        name=details.name,
        algorithm_type="key encapsulation mechanism",
        family="code based",
        nist_security_category=details.claimed_nist_level,
        standardization="NIST selected for standardization; FIPS not yet finalized",
        implementation_version=details.version,
        public_key_length=details.public_key_length,
        secret_key_length=details.secret_key_length,
        ciphertext_length=details.ciphertext_length,
        shared_secret_length=details.shared_secret_length,
    )


@dataclass(frozen=True, slots=True, repr=False)
class HQC3(OQSKEMProvider):
    """Private ephemeral HQC-3 capability backed by liboqs."""

    ALGORITHM: ClassVar[str] = HQC_3_ALGORITHM

    @classmethod
    def algorithm_metadata(cls) -> KEMMetadata:
        """Return selected and backend-derived HQC-3 metadata."""

        return hqc_3_metadata()
