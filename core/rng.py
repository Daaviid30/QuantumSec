#================= QUANTUM SEC ===================

# @ AUTHOR: David Martín Castro
# @ GITHUB: https://github.com/Daaviid30

#=================================================

#================= IMPORT MODULES =================
from abc import ABC, abstractmethod

import numpy as np
from scipy.stats import unitary_group


class BaseRNG(ABC):
    """
    Abstract base class ensuring all RNGs expose the same NumPy Generator interface.
    Any Random Number Generator must expose a gen property that returns
    a NumPy random generator object
    """
    
    @property
    @abstractmethod
    def gen(self) -> np.random.Generator:
        pass

# ==========================================
# 2. Core RNG Classes
# ==========================================
class SeededRNG(BaseRNG):
    """Deterministic PRNG for reproducible Monte Carlo simulations and unit tests."""
    def __init__(self, seed: int):
        # PCG-64 is the default underlying bit generator in modern NumPy
        self._gen = np.random.default_rng(seed)

    @property
    def gen(self) -> np.random.Generator:
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
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Without a seed, default_rng pulls from OS entropy
            cls._instance._gen = np.random.default_rng() 
        return cls._instance

    @property
    def gen(self) -> np.random.Generator:
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
        :param base_rng: The underlying PRNG (Seeded or Global) driving the simulation.
        :param bias_prob: Probability of generating a '1' (Ideal is 0.5). Models detector imbalance.
        :param correlation: Markovian transition modifier. Models thermal/electronic memory.
                            0.0 means independent bits. >0 means bits tend to repeat.
        """
        self.base_rng = base_rng
        self.bias_prob = bias_prob
        self.correlation = correlation

    @property
    def gen(self) -> np.random.Generator:
        # We still expose the raw generator if absolutely necessary, 
        # but usage should go through specific QRNG methods.
        return self.base_rng.gen

    def generate_raw_bits(self, size: int) -> np.ndarray:
        """Generates bits incorporating physical bias and classical readout correlation."""
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
    """Generates a perfectly random classical bit (0 or 1)."""
    return rng.gen.integers(0, 2, size=size)

def random_basis(rng: BaseRNG, size: int | None = None) -> int | np.ndarray:
    """
    Generates a random basis choice. 
    Convention: 0 represents Rectilinear (Z), 1 represents Diagonal (X).
    """
    return rng.gen.integers(0, 2, size=size)

def random_unitary(rng: BaseRNG, dimension: int) -> np.ndarray:
    """
    Generates a random NxN unitary matrix distributed according to the Haar measure.
    Crucial for simulating arbitrary quantum channels, noise, or Eve's attacks.
    
    :param rng: The BaseRNG instance.
    :param dimension: The dimension of the Hilbert space (e.g., 2 for a single qubit).
    """
    # SciPy's unitary_group requires a NumPy RandomState or Generator seed.
    # We pass the exact NumPy generator from our injected RNG.
    return unitary_group.rvs(dim=dimension, random_state=rng.gen)