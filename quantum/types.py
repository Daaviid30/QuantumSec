"""Shared NumPy typing aliases for quantum numerical APIs."""

import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike
ComplexArray = npt.NDArray[np.complex128]
RealArray = npt.NDArray[np.float64]
