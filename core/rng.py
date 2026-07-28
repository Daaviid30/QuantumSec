#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================
from abc import ABC, abstractmethod

import numpy as np


class BaseRNG(ABC):
    """
    Abstract base class ensuring all RNGs expose the same NumPy Generator interface.
    Any Random Number Generator must expose a gen property that returns
    a NumPy random generator object
    """
    
    @property
    @abstractmethod
    def gen(self) -> np.random.Generator:
        """
        Provide the NumPy generator used by the random source.

        Parameters:
        -----------
        None.

        Returns:
        --------
        np.random.Generator
            Generator that supplies random values.

        Raises:
        -------
        None.
        """
        pass

# ==========================================
# 2. Core RNG Classes
# ==========================================
class SeededRNG(BaseRNG):
    """Deterministic PRNG for reproducible Monte Carlo simulations and unit tests."""
    def __init__(self, seed: int):
        """
        Initialize a reproducible random number generator.

        Parameters:
        -----------
        seed: int
            Non-negative seed used to initialize NumPy's generator.

        Returns:
        --------
        None.

        Raises:
        -------
        ValueError
            If the seed is not valid for NumPy's generator.
        """
        # PCG-64 is the default underlying bit generator in modern NumPy
        self._gen = np.random.default_rng(seed)

    @property
    def gen(self) -> np.random.Generator:
        """
        Return the seeded NumPy generator.

        Parameters:
        -----------
        None.

        Returns:
        --------
        np.random.Generator
            Generator initialized with this instance's seed.

        Raises:
        -------
        None.
        """
        return self._gen


class GlobalRNG(BaseRNG):
    """
    Singleton for production. Draws seed from OS entropy (/dev/urandom).
    Strictly for deployment runs where reproducibility is fundamentally unwanted.
    """
    # We indicate that these variables are None sometimes, in order to prevent syntax errors, 
    # as they will be initialized in the __new__ method.
    _instance: GlobalRNG | None = None
    _gen: np.random.Generator | None = None 

    # Singleton pattern, ensures only one instance of GlobalRNG is created and used throughout the application
    # This is useful for performance reasons and for ensuring that the same random number generator is used
    def __new__(cls):
        """
        Create or return the process-wide random generator singleton.

        Parameters:
        -----------
        None.

        Returns:
        --------
        GlobalRNG
            Shared global random number generator instance.

        Raises:
        -------
        None.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Without a seed, default_rng pulls from OS entropy
            cls._instance._gen = np.random.default_rng() 
        return cls._instance

    @property
    def gen(self) -> np.random.Generator:
        """
        Return the singleton's entropy-seeded NumPy generator.

        Parameters:
        -----------
        None.

        Returns:
        --------
        np.random.Generator
            Shared generator initialized from operating-system entropy.

        Raises:
        -------
        AssertionError
            If the singleton generator was not initialized correctly.
        """
        # Confirmation that _gen is not None, this is for the type hints
        assert self._gen is not None, "Generator was not initialized"
        return self._gen


class QRNGSimulator(BaseRNG):
    """
    Simulates a physical Quantum Random Number Generator.
    Injects realistic physical imperfections (bias and Markovian correlation).
    """
    def __init__(self, base_rng: BaseRNG, bias_prob: float = 0.5, correlation: float = 0.0):
        """
        Initialize a quantum random number generator simulator.

        Parameters:
        -----------
        base_rng: BaseRNG
            Random source that drives the simulation.
        bias_prob: float
            Probability of producing one; 0.5 represents an unbiased source.
        correlation: float
            Markovian correlation modifier; positive values favor repeated bits.

        Returns:
        --------
        None.

        Raises:
        -------
        None.
        """
        self.base_rng = base_rng
        self.bias_prob = bias_prob
        self.correlation = correlation

    @property
    def gen(self) -> np.random.Generator:
        """
        Return the NumPy generator supplied by the base random source.

        Parameters:
        -----------
        None.

        Returns:
        --------
        np.random.Generator
            Generator used to simulate raw quantum measurements.

        Raises:
        -------
        None.
        """
        # We still expose the raw generator if absolutely necessary, 
        # but usage should go through specific QRNG methods.
        return self.base_rng.gen

    def generate_raw_bits(self, size: int) -> np.ndarray:
        """
        Generate raw bits with the configured bias and temporal correlation.

        Parameters:
        -----------
        size: int
            Number of bits to generate.

        Returns:
        --------
        np.ndarray
            One-dimensional integer array containing zeros and ones.

        Raises:
        -------
        ValueError
            If size is negative or bias_prob is outside the interval [0, 1].
        """
        if size < 0:
            raise ValueError("[!] Size must be non-negative.")

        if size == 0:
            return np.array([], dtype=int)

        if self.correlation == 0.0:
            # Simple biased coin flip (Bernoulli trials)
            return self.gen.binomial(n=1, p=self.bias_prob, size=size)
        
        # Markov chain approach for temporal correlation (electronic noise)
        bits = np.zeros(size, dtype=int)
        # Initial bit based on pure bias
        bits[0] = self.gen.binomial(n=1, p=self.bias_prob)
        
        # Generate transition probabilities
        for i in range(1, size):
            # If correlation is positive, probability shifts towards previous bit
            # This is a simplified model suitable for TFM simulation of readout noise
            p_stay = 0.5 + (self.correlation / 2)
            if bits[i-1] == 1:
                # This is a mathematical formulation to compensate for the bias probability
                # and the correlation in the same equation. It is not the most optimal 
                # way to do it, but it is a valid one for simulation purposes.
                p_one = p_stay if self.bias_prob >= 0.5 else p_stay * (self.bias_prob / 0.5)
            else:
                p_one = (1 - p_stay) if self.bias_prob <= 0.5 else (1 - p_stay) * (self.bias_prob / 0.5)
            
            # Clamp probabilities to valid [0, 1] range
            p_one = max(0.0, min(1.0, p_one))
            bits[i] = self.gen.binomial(n=1, p=p_one)
            
        return bits

# ==========================================
# 3. Cryptographic Helper Functions
# ==========================================
# Notice how every helper REQUIRES an rng instance to be passed in.

# If size is None, numpy returns only one random number. 
def random_bit(rng: BaseRNG, size: int | None = None) -> int | np.ndarray:
    """
    Generate one or more uniformly distributed classical bits.

    Parameters:
    -----------
    rng: BaseRNG
        Random source used to generate the bits.
    size: int | None
        Number of bits to return, or None for a scalar bit.

    Returns:
    --------
    int | np.ndarray
        Scalar bit or one-dimensional array containing zeros and ones.

    Raises:
    -------
    ValueError
        If size is negative.
    """
    return rng.gen.integers(0, 2, size=size)

def random_basis(rng: BaseRNG, size: int | None = None) -> int | np.ndarray:
    """
    Generate one or more random quantum-basis choices.

    Parameters:
    -----------
    rng: BaseRNG
        Random source used to choose the bases.
    size: int | None
        Number of choices to return, or None for a scalar choice.

    Returns:
    --------
    int | np.ndarray
        Basis choice where 0 denotes the Z basis and 1 denotes the X basis.

    Raises:
    -------
    ValueError
        If size is negative.
    """
    return rng.gen.integers(0, 2, size=size)

def random_unitary(rng: BaseRNG, dimension: int) -> np.ndarray:
    """
    Generate a Haar-distributed random unitary matrix.

    Parameters:
    -----------
    rng: BaseRNG
        Random source used to generate the underlying complex matrix.
    dimension: int
        Positive dimension of the square unitary matrix.

    Returns:
    --------
    np.ndarray
        Complex unitary matrix with shape (dimension, dimension).

    Raises:
    -------
    ValueError
        If dimension is not positive.
    """
    if dimension <= 0:
        raise ValueError("[!] Dimension must be positive.")

    # QR decomposition of a complex Ginibre matrix produces a Haar-distributed
    # unitary after correcting the arbitrary phases on R's diagonal.
    matrix = rng.gen.normal(size=(dimension, dimension)) + 1j * rng.gen.normal(
        size=(dimension, dimension)
    )
    unitary, triangular = np.linalg.qr(matrix)
    diagonal = np.diag(triangular)
    phases = diagonal / np.abs(diagonal)

    return unitary * phases.conj()
