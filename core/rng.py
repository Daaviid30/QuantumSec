"""Injectable random-number sources for reproducible simulations."""

from abc import ABC, abstractmethod

import numpy as np


class BaseRNG(ABC):
    """Common interface for random sources backed by a NumPy generator."""

    @property
    @abstractmethod
    def gen(self) -> np.random.Generator:
        """Return the underlying NumPy generator."""

        raise NotImplementedError

    def random_bits(self, size: int | None = None) -> np.integer | np.ndarray:
        """Generate binary choices, allowing specialized RNGs to override their model."""

        return self.gen.integers(0, 2, size=size)


class SeededRNG(BaseRNG):
    """Deterministic PRNG for reproducible simulations and tests."""

    def __init__(self, seed: int):
        self._gen = np.random.default_rng(seed)

    @property
    def gen(self) -> np.random.Generator:
        """Return the generator initialized with this instance's seed."""

        return self._gen


class GlobalRNG(BaseRNG):
    """Process-wide generator initialized from operating-system entropy."""

    _instance: GlobalRNG | None = None
    _gen: np.random.Generator | None = None

    def __new__(cls) -> GlobalRNG:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._gen = np.random.default_rng()
        return cls._instance

    @property
    def gen(self) -> np.random.Generator:
        """Return the shared entropy-seeded NumPy generator."""

        assert self._gen is not None, "Generator was not initialized"
        return self._gen


class QRNGSimulator(BaseRNG):
    """Simulate a physical QRNG with bias and Markovian correlation."""

    def __init__(
        self,
        base_rng: BaseRNG,
        bias_prob: float = 0.5,
        correlation: float = 0.0,
    ):
        self.base_rng = base_rng
        self.bias_prob = bias_prob
        self.correlation = correlation

    @property
    def gen(self) -> np.random.Generator:
        """Return the generator supplied by the base random source."""

        return self.base_rng.gen

    def generate_raw_bits(self, size: int) -> np.ndarray:
        """Generate raw bits with the configured bias and temporal correlation."""

        if isinstance(size, (bool, np.bool_)) or not isinstance(size, (int, np.integer)):
            raise ValueError(f"Size must be a non-negative integer. Got size={size!r}.")
        clean_size = int(size)
        if clean_size < 0:
            raise ValueError(f"Size must be non-negative. Got size={size}.")
        if not 0.0 <= self.bias_prob <= 1.0:
            raise ValueError(f"Bias probability must lie in [0, 1]. Got {self.bias_prob}.")
        if not -1.0 <= self.correlation <= 1.0:
            raise ValueError(f"Correlation must lie in [-1, 1]. Got {self.correlation}.")
        if clean_size == 0:
            return np.array([], dtype=int)
        if self.correlation == 0.0:
            return self.gen.binomial(n=1, p=self.bias_prob, size=clean_size)

        bits = np.zeros(clean_size, dtype=int)
        bits[0] = self.gen.binomial(n=1, p=self.bias_prob)
        p_one_after_one = self.bias_prob + self.correlation * (1.0 - self.bias_prob)
        p_one_after_zero = self.bias_prob * (1.0 - self.correlation)

        for index in range(1, clean_size):
            p_one = p_one_after_one if bits[index - 1] == 1 else p_one_after_zero
            bits[index] = self.gen.binomial(n=1, p=float(np.clip(p_one, 0.0, 1.0)))

        return bits

    def random_bits(self, size: int | None = None) -> np.integer | np.ndarray:
        """Generate binary choices using this simulator's bias/correlation model."""

        if size is None:
            return np.int64(self.generate_raw_bits(1)[0])
        return self.generate_raw_bits(size)


def random_bit(rng: BaseRNG, size: int | None = None) -> np.integer | np.ndarray:
    """Generate one or more uniformly distributed classical bits."""

    return rng.random_bits(size=size)


def random_basis(rng: BaseRNG, size: int | None = None) -> np.integer | np.ndarray:
    """Generate generic binary choices for adaptation by the QKD layer."""

    return rng.random_bits(size=size)


def random_unitary(rng: BaseRNG, dimension: int) -> np.ndarray:
    """Generate a Haar-distributed random unitary using QR decomposition."""

    if dimension <= 0:
        raise ValueError(f"Dimension must be positive. Got dimension={dimension}.")

    matrix = rng.gen.normal(size=(dimension, dimension)) + 1j * rng.gen.normal(size=(dimension, dimension))
    unitary, triangular = np.linalg.qr(matrix)
    diagonal = np.diag(triangular)
    phases = diagonal / np.abs(diagonal)
    return unitary * phases.conj()
