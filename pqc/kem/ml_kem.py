"""ML-KEM-768 key encapsulation executed by liboqs."""

from dataclasses import dataclass
from functools import cache
from typing import ClassVar, Final

from pqc.backends.oqs_kem_backend import OQSKEMBackend
from pqc.errors import BackendOperationError
from pqc.kem._oqs_provider import OQSKEMProvider
from pqc.kem.base import KEMMetadata

ML_KEM_768_ALGORITHM: Final = "ML-KEM-768"


@cache
def ml_kem_768_metadata() -> KEMMetadata:
    """Return backend-derived ML-KEM-768 metadata."""

    details = OQSKEMBackend().details(ML_KEM_768_ALGORITHM)
    if details.name != ML_KEM_768_ALGORITHM or details.claimed_nist_level != 3:
        raise BackendOperationError("liboqs returned inconsistent ML-KEM-768 metadata.")
    return KEMMetadata(
        name=details.name,
        algorithm_type="key encapsulation mechanism",
        family="module-lattice based",
        nist_security_category=details.claimed_nist_level,
        standardization="NIST FIPS 203",
        implementation_version=details.version,
        public_key_length=details.public_key_length,
        secret_key_length=details.secret_key_length,
        ciphertext_length=details.ciphertext_length,
        shared_secret_length=details.shared_secret_length,
    )


@dataclass(frozen=True, slots=True, repr=False)
class MLKEM768(OQSKEMProvider):
    """Private ephemeral ML-KEM-768 capability backed by liboqs."""

    ALGORITHM: ClassVar[str] = ML_KEM_768_ALGORITHM

    @classmethod
    def algorithm_metadata(cls) -> KEMMetadata:
        """Return standardized and backend-derived ML-KEM-768 metadata."""

        return ml_kem_768_metadata()
