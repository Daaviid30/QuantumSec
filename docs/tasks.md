# QuantumSec — Development Task Roadmap

> Scope: quantum primitives, projective measurements, quantum-information utilities, validation, tests, and performance.

## Status legend

- `[x]` Completed.
- `[ ]` Pending.
- **P0** — correctness or API blocker.
- **P1** — core architecture and tests.
- **P2** — performance and maintainability.
- **P3** — repository cleanup and future work.

---

## Current state

- [x] Pure-state ket validation and normalization utilities.
- [x] Density-matrix construction from kets and ensembles.
- [x] Density-matrix validation: square, finite, Hermitian, unit trace, and positive semidefinite.
- [x] Individual orthogonal-projector validation: square, finite, Hermitian, and idempotent.
- [x] Complete projective-measurement validation using individual validation plus `sum(P_i) = I`.
- [x] General projective measurement using Born probabilities and Lüders state update.
- [x] `is_projective_measurement()` fixed so the internal validation function is actually called.

---

# P0 — Measurement correctness and API refactor

## 1. Improve `MeasurementResult`

- [ ] Update the dataclass to avoid unsafe NumPy-array equality and large representations.

```python
from dataclasses import dataclass, field

import numpy as np


@dataclass(frozen=True, slots=True, eq=False)
class MeasurementResult:
    outcome: int
    probability: float
    post_state: np.ndarray = field(repr=False)
```

### Work required

- Add `eq=False`; automatic dataclass equality does not work safely with `np.ndarray`.
- Add `field(repr=False)` so printing a result does not dump the full density matrix.
- Keep `frozen=True` and `slots=True`.
- Compare result arrays explicitly in tests with `numpy.testing.assert_allclose`.

### Acceptance criteria

- The object remains immutable.
- Its representation is compact.
- Tests do not use `result_a == result_b`.

---

## 2. Add `MeasurementSample`

- [ ] Create a lightweight result for sampling an outcome without constructing a collapsed state.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MeasurementSample:
    index: int
    outcome: int
    probability: float
```

### Purpose

- `index` identifies the selected projector.
- `outcome` is the logical value returned to the protocol.
- `probability` is the Born probability of that outcome.
- `sample_projective_outcome()` returns this object without evaluating `P @ rho @ P`.

---

## 3. Create `ProjectiveMeasurement`

- [ ] Add an immutable class representing a complete projective measurement validated exactly once.

Recommended location: `quantum/measures.py`.

```python
from dataclasses import dataclass

import numpy as np

from quantum import validation as v


@dataclass(frozen=True, slots=True, eq=False)
class ProjectiveMeasurement:
    projectors: tuple[np.ndarray, ...]
    outcomes: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.projectors) == 0:
            raise ValueError("A projective measurement requires projectors.")

        if len(self.projectors) != len(self.outcomes):
            raise ValueError(
                "Each projector must have one associated outcome. "
                f"Got {len(self.projectors)} projectors and "
                f"{len(self.outcomes)} outcomes."
            )

        clean_projectors = tuple(
            np.array(projector, dtype=np.complex128, copy=True)
            for projector in self.projectors
        )

        v.validate_projective_measurement(clean_projectors)

        for projector in clean_projectors:
            projector.flags.writeable = False

        object.__setattr__(self, "projectors", clean_projectors)
        object.__setattr__(self, "outcomes", tuple(self.outcomes))

    @property
    def dimension(self) -> int:
        return self.projectors[0].shape[0]

    @property
    def number_of_outcomes(self) -> int:
        return len(self.projectors)
```

### Work required

- Reject empty projector collections.
- Require one outcome per projector.
- Copy every projector to `np.complex128`.
- Call `validate_projective_measurement()` inside `__post_init__`.
- Make all stored projector arrays read-only.
- Store projectors and outcomes as tuples.

### Why

The object becomes a trusted, prevalidated measurement:

```text
construct once -> validate once -> reuse for every signal
```

### Acceptance criteria

- Invalid or incomplete measurements fail during construction.
- Stored projectors cannot be modified.
- Per-signal measurement no longer validates individual projectors.

---

## 4. Refactor `measure_projective()`

- [ ] Make the function receive `ProjectiveMeasurement` instead of `Sequence[np.ndarray]`.

```python
def measure_projective(
    rho: np.ndarray,
    measurement: ProjectiveMeasurement,
    rng: BaseRNG,
    tol: float = ATOL,
    validate_state: bool = True,
) -> MeasurementResult:
    ...
```

### Remove from the hot path

- Empty projector checks.
- Repeated projector conversion.
- Repeated `validate_projector()` calls.
- Repeated complete-measurement validation.

### Keep per signal

- Density-matrix conversion.
- Optional density-matrix validation.
- Shape compatibility.
- Born-probability calculation.
- Probability range and normalization checks.
- RNG sampling.
- Lüders update when a post-state is requested.

### Dimension check

```python
expected_shape = (measurement.dimension, measurement.dimension)

if rho.shape != expected_shape:
    raise ValueError(
        "Measurement and state dimensions must match. "
        f"Got measurement dimension={measurement.dimension} "
        f"and rho.shape={rho.shape}."
    )
```

### Zero-probability protection

```python
if sample.probability <= tol:
    raise RuntimeError(
        "Sampled an outcome with numerically zero probability."
    )
```

---

## 5. Validate probabilities before `np.clip`

- [ ] Replace unconditional clipping with validation followed by numerical cleanup.

Correct order:

1. Calculate all Born probabilities.
2. Reject a significant imaginary part.
3. Reject values below `-tol`.
4. Reject values above `1 + tol`.
5. Clip only tiny numerical residues.
6. Check that the total is one within tolerance.
7. Normalize by the total.

```python
if np.any(probabilities < -tol):
    raise ValueError(
        "Measurement probabilities must be non-negative. "
        f"Got {probabilities}."
    )

if np.any(probabilities > 1.0 + tol):
    raise ValueError(
        "Measurement probabilities cannot exceed one. "
        f"Got {probabilities}."
    )

probabilities = np.clip(probabilities, 0.0, 1.0)

total_probability = float(np.sum(probabilities))

if not np.isclose(total_probability, 1.0, atol=tol, rtol=0.0):
    raise ValueError(
        "Measurement probabilities must sum to one. "
        f"Got {total_probability}."
    )

probabilities /= total_probability
```

### Reason

An invalid vector such as `[-0.1, 1.1]` sums to one. Direct clipping would hide a physical error by converting it into `[0.0, 1.0]`.

---

## 6. Add `validate_state`

- [ ] Add `validate_state: bool = True` to sampling and full-measurement functions.

```python
if validate_state:
    v.validate_density_matrix(rho, tol)
```

### Behaviour

- Default to `True` for development, unit tests, notebooks, and safe public use.
- Use `False` in large experiments only after channels and state-producing paths have physics-preservation tests.
- Even with `False`, retain cheap checks:
  - shape compatibility;
  - real probabilities;
  - probability range;
  - total probability equal to one.

### Reason

`validate_density_matrix()` performs `np.linalg.eigvalsh`, approximately `O(d^3)`. Repeating it across very large signal sets may dominate runtime.

---

## 7. Separate sampling and collapse

- [ ] Implement `sample_projective_outcome()`.
- [ ] Make `measure_projective()` call it and then calculate the post-state.

```python
def sample_projective_outcome(
    rho: np.ndarray,
    measurement: ProjectiveMeasurement,
    rng: BaseRNG,
    tol: float = ATOL,
    validate_state: bool = True,
) -> MeasurementSample:
    ...
```

### `sample_projective_outcome()` responsibilities

- Convert `rho` to `np.complex128`.
- Optionally validate `rho`.
- Check dimensional compatibility.
- Compute and validate Born probabilities.
- Sample one outcome through the injected RNG.
- Return `MeasurementSample`.
- Do not calculate a collapsed state.

### `measure_projective()` responsibilities

- Call `sample_projective_outcome()`.
- Retrieve `measurement.projectors[sample.index]`.
- Calculate:

```python
post_state = projector @ rho @ projector
post_state /= sample.probability
```

- Return `MeasurementResult`.

### Usage

Use `sample_projective_outcome()` when the system is discarded and only the logical result matters, as in most final Bob measurements in BB84.

Use `measure_projective()` for intercept-resend, repeated measurements, demonstrations, debugging, and stateful simulations.

---

# P1 — Bases and standard QKD measurements

## 8. Create `Basis`

- [ ] Create `qkd/primitives/bases.py`.

```python
from enum import Enum


class Basis(Enum):
    Z = "Z"
    X = "X"
    Y = "Y"
```

### Work required

- Replace unexplained integer conventions in protocol code.
- Add an adapter from random integers to `Basis` values at the QKD layer.
- Keep low-level RNG utilities generic.
- Export `Basis` from `qkd/primitives/__init__.py` when stable.

### Acceptance criteria

- BB84 uses `Basis.Z` and `Basis.X`, not magic numbers.
- Conversion helpers are covered by tests.

---

## 9. Create standard measurements

- [ ] Create `qkd/primitives/measurements.py`.

Define reusable instances:

```python
MEASUREMENT_Z = ProjectiveMeasurement(
    projectors=(P0, P1),
    outcomes=(0, 1),
)

MEASUREMENT_X = ProjectiveMeasurement(
    projectors=(P_PLUS, P_MINUS),
    outcomes=(0, 1),
)

MEASUREMENT_Y = ProjectiveMeasurement(
    projectors=(P_I, P_MINUS_I),
    outcomes=(0, 1),
)
```

Map bases to instances:

```python
MEASUREMENTS_BY_BASIS = {
    Basis.Z: MEASUREMENT_Z,
    Basis.X: MEASUREMENT_X,
    Basis.Y: MEASUREMENT_Y,
}
```

### Architectural boundary

- `quantum/measures.py`: general measurement mathematics and domain classes.
- `qkd/primitives/measurements.py`: QKD-specific predefined instances.
- `qkd/protocols/bb84.py`: chooses Z or X only.

---

# P1 — Quantum information module

## 10. Create `quantum/information.py`

- [ ] Move purity out of `quantum/measures.py`.
- [ ] Add purity, trace distance, fidelity, and von Neumann entropy.

### Purity

```python
def purity(
    rho: np.ndarray,
    tol: float = ATOL,
    validate_state: bool = True,
) -> float:
    if validate_state:
        v.validate_density_matrix(rho, tol)

    value = np.trace(rho @ rho)
    return float(value.real)
```

### Trace distance

```text
D(rho, sigma) = 1/2 ||rho - sigma||_1
```

For Hermitian `rho - sigma`:

```python
eigenvalues = np.linalg.eigvalsh(rho - sigma)
return 0.5 * float(np.sum(np.abs(eigenvalues)))
```

Requirements:

- Same shapes.
- Optional validation of both states.
- Real result in `[0, 1]` within tolerance.

### Fidelity

Use and document squared Uhlmann fidelity:

```text
F(rho, sigma) = (Tr sqrt(sqrt(rho) sigma sqrt(rho)))^2
```

Requirements:

- Internal positive-semidefinite matrix square-root helper using `np.linalg.eigh`.
- Clip only tiny negative eigenvalues within tolerance.
- Reject significant negativity.
- Symmetrize intermediate Hermitian matrices when necessary.
- Use one fidelity convention throughout the project.

### Von Neumann entropy

```text
S(rho) = -sum(lambda_i log2(lambda_i))
```

Requirements:

- Use `np.linalg.eigvalsh`.
- Ignore eigenvalues numerically equal to zero.
- Return entropy in bits.
- Reject significant negative eigenvalues when validation is disabled.

---

# P1 — Tests required before BB84

## 11. Projector validation

- [ ] Valid rank-one projectors are accepted.
- [ ] Higher-rank orthogonal projectors are accepted.
- [ ] Non-square arrays are rejected.
- [ ] Non-Hermitian matrices are rejected.
- [ ] Hermitian but non-idempotent matrices are rejected.
- [ ] Empty and non-finite inputs are rejected.

## 12. Complete projective measurements

- [ ] `(P0, P1)` is valid.
- [ ] `(P_PLUS, P_MINUS)` is valid.
- [ ] `(P0, P0)` is rejected.
- [ ] `(P0,)` is rejected for a two-dimensional space.
- [ ] Mixed dimensions are rejected.
- [ ] Invalid projector errors identify the sequence index.
- [ ] `is_projective_measurement()` returns the expected boolean.

## 13. `ProjectiveMeasurement`

- [ ] Valid construction succeeds.
- [ ] Mismatched projector and outcome counts fail.
- [ ] Invalid sets fail during construction.
- [ ] Input arrays are copied.
- [ ] Stored arrays are read-only.
- [ ] `dimension` is correct.
- [ ] `number_of_outcomes` is correct.

## 14. Sampling

- [ ] `|0><0|` measured in Z always returns 0 with probability 1.
- [ ] `|1><1|` measured in Z always returns 1 with probability 1.
- [ ] `|+><+|` measured in X always returns the plus outcome.
- [ ] The maximally mixed qubit has Z probabilities `[0.5, 0.5]`.
- [ ] Equal seeds produce equal sampled sequences.
- [ ] `validate_state=False` skips spectral validation but keeps probability checks.
- [ ] Invalid probability ranges fail before clipping.

## 15. Collapse

- [ ] Measuring `|+><+|` in Z collapses to `|0><0|` or `|1><1|`.
- [ ] The post-state has trace one.
- [ ] The post-state is Hermitian and positive semidefinite.
- [ ] Repeating the same measurement returns the same outcome with probability one.
- [ ] Sampling and full measurement select the same index with equal seeded RNG streams.

## 16. Quantum information

### Purity

- [ ] Pure state: `1.0`.
- [ ] Maximally mixed qubit: `0.5`.
- [ ] Maximally mixed dimension four: `0.25`.

### Trace distance

- [ ] Equal states: `0.0`.
- [ ] Orthogonal pure states: `1.0`.
- [ ] Symmetry.

### Fidelity

- [ ] Equal states: `1.0`.
- [ ] Orthogonal pure states: `0.0`.
- [ ] Symmetry within tolerance.
- [ ] Pure-state analytical overlap case.

### Von Neumann entropy

- [ ] Pure state: `0.0` bits.
- [ ] Maximally mixed qubit: `1.0` bit.
- [ ] Maximally mixed dimension four: `2.0` bits.

---

# P2 — Performance and maintainability

## 17. Benchmark safe and fast paths

- [ ] Compare `validate_state=True` and `False` for `10^3`, `10^4`, and `10^5` one-qubit signals.
- [ ] Measure time spent in `validate_density_matrix()` and `eigvalsh`.
- [ ] Use benchmark evidence before introducing vectorized or JIT implementations.

Optimization order:

1. Stop revalidating constant projectors.
2. Avoid post-state construction when only an outcome is required.
3. Make density spectral validation optional.
4. Then evaluate `einsum`, batching, or alternative backends.

## 18. Add NumPy type aliases

- [ ] Create `quantum/types.py` if useful.

```python
import numpy as np
import numpy.typing as npt

ArrayLike = npt.ArrayLike
ComplexArray = npt.NDArray[np.complex128]
RealArray = npt.NDArray[np.float64]
```

Do not create wrapper classes for ket, density matrix, projector, or probability vector yet.

## 19. Centralize tolerance

- [ ] Move repeated `ATOL = 1e-10` declarations to `core/constants.py`.

```python
DEFAULT_ATOL = 1e-10
```

The constants module must not import quantum or QKD modules.

---

# P3 — Repository quality and future work

## 20. Clean messages and spelling

- [ ] Correct `proyector`, `bi-dimensional`, and `projecctor`.
- [ ] Use `Hermitian` consistently.
- [ ] Include useful dimensions, shapes, indices, and values in errors.
- [ ] Ensure `is_*` docstrings match actual malformed-input behaviour.

## 21. Simplify excessive docstrings

- [ ] Remove `Parameters: None` and `Raises: None` sections.
- [ ] Keep scientific public APIs fully documented.
- [ ] Keep trivial properties concise.
- [ ] Use one NumPy-style format consistently.

## 22. Review dependencies

- [ ] Replace the placeholder `pyproject.toml` description.
- [ ] Review Qiskit as a mandatory dependency.
- [ ] Move it to an optional group if used only for comparisons, notebooks, or external validation.

## 23. Delay unnecessary wrappers

- [ ] Do not create `QuantumState`, `Ket`, `DensityMatrix`, `Projector`, or `ProbabilityVector` wrapper classes yet.

Revisit only if the project later requires multiple numerical backends, state metadata, strict serialization, cached decompositions, or backend-independent methods.

## 24. Preserve room for POVMs

- [ ] Keep APIs explicitly named `ProjectiveMeasurement`, `sample_projective_outcome`, and `measure_projective`.
- [ ] Do not create a generic hierarchy until B92 introduces a real second measurement model.
- [ ] Design POVM effects and measurement operators separately; POVM effects are not necessarily idempotent or orthogonal.

---

# Recommended implementation order

1. [ ] Update `MeasurementResult`.
2. [ ] Add `MeasurementSample`.
3. [ ] Implement `ProjectiveMeasurement` and tests.
4. [ ] Create `Basis` in `qkd/primitives/bases.py`.
5. [ ] Create standard Z/X/Y measurements.
6. [ ] Fix probability validation before clipping.
7. [ ] Implement `sample_projective_outcome()`.
8. [ ] Refactor `measure_projective()` to reuse sampling.
9. [ ] Add `validate_state` to both paths.
10. [ ] Create `quantum/information.py` and move purity.
11. [ ] Implement trace distance, fidelity, and von Neumann entropy.
12. [ ] Complete measurement and information tests.
13. [ ] Benchmark safe and fast paths.

---

# Definition of done

This development block is complete when:

- Standard projective measurements are validated once and immutable.
- Per-signal sampling performs no repeated projector validation.
- Outcome-only sampling avoids unnecessary collapse products.
- Full measurement returns a normalized post-state.
- Expensive density validation can be disabled explicitly for large experiments.
- Probability clipping cannot hide invalid physical values.
- Purity, fidelity, trace distance, and von Neumann entropy live in `quantum/information.py` and have analytical tests.
- All randomness remains reproducible through injected `BaseRNG` instances.
- Ruff, Pyright, and Pytest pass for all modified modules.
