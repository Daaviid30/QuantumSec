import numpy as np 

# How to create vectors in numpy
ket0 = np.array([[1],[0]])
ket1 = np.array([[0],[1]])
bra0 = np.array([[1,0]])
bra1 = np.array([[0,1]])

# How to calculate complex conjugates (hermitian conjugates)
bra_0 = np.conjugate(ket0.T)

# We can create matrices too
I = np.array([[1,0],[0,1]])
X = np.array([[0,1],[1,0]])
Y = np.array([[0,-1j],[1j,0]])
Z = np.array([[1,0],[0,-1]])

# We could applay the hermitian conjugate into matrices too
adjoint_Y = np.conjugate(Y.T)

# A matrix multiplication is represented like:
mul_XY = np.matmul(X,Y)

# -------------- COMPLETENESS RELATION ----------
# We are going to proof the completeness relation with the standard basis on the Hilbert space of a qubit
# First, we calculate the projectors
P0 = np.matmul(ket0, bra0) # |0><0|
P1 = np.matmul(ket1,bra1) # |1><1|

# The sum of the projectors has to be equal to the identity matrix
completeness = P0 + P1
#print(completeness)

# --------------- EIGENVALUES / EIGENVECTORS --------
# With numpy we are able to obtein the eigenvalues and eigenvectors of an operator
eigenvalues_Z, eigenvectors_Z = np.linalg.eigh(Z)
#print(f"Eigenvalues: {eigenvalues_Z}\nEigenvectors: {eigenvectors_Z}")


# --------------- MEASUREMENTS ----------------------
# We are going to simulate the measurement of a vector on the standard basis
standard_basis = [P0, P1]
plus_ket_state = np.array([[1/np.sqrt(2)],[1/np.sqrt(2)]])
plus_bra_state = np.conjugate(plus_ket_state.T)

measurement_probabilities = []
for projector in standard_basis:
    measurement_probabilities.append(np.matmul((np.matmul(plus_bra_state, projector)), plus_ket_state))

#print(measurement_probabilities)


# ---------------- COMPOSITE SYSTEMS -----------------
tensor_01 = np.kron(ket0, ket1) # Kron function it is the tensor product
#print(tensor_01) # We get an |01> vector from this operartion

# Computational basis for a 2-qubit system
ket00 = np.kron(ket0, ket0)
ket01 = np.kron(ket0, ket1)
ket10 = np.kron(ket1, ket0)
ket11 = np.kron(ket1, ket1)
#print(f"2-Qubit basis:")
#print(f"|00>:\n{ket00}\n|01>:\n{ket01}\n|10>:\n{ket10}\n|11>:\n{ket11}")

# We can use the tensor product on operations too
operator_YZ = np.kron(Y, Z)
#print(operator_YZ)

# Bell basis (entangled states)
phi_plus = (ket00 + ket11) / np.sqrt(2)
phi_minus = (ket00 - ket11) / np.sqrt(2)
psi_plus = (ket01 + ket10) / np.sqrt(2)
psi_minus = (ket01 - ket10) / np.sqrt(2)
#print(f"BELL BASIS:\n{phi_plus}\n{phi_minus}\n{psi_plus}\n{psi_minus}")

# ------------------ DENSITY MATRIX ----------------------
density_matrix_0 = ket0 @ bra0 # Another way to do a matrix multiplication
#print(density_matrix_0)

mixed_state = np.array([[0.5, 0],[0, 0.5]])
#print(mixed_state)

# Trace calculation, in order to check if they are physical states (Trace = 1)
trace_0 = np.trace(density_matrix_0)
trace_mixed = np.trace(mixed_state)

# Purity calculation, in order to check the type of the state.
purity_0 = np.trace(density_matrix_0 @ density_matrix_0) # p^2
purity_mixed = np.trace(mixed_state @ mixed_state)

print(trace_mixed, trace_0, purity_0, purity_mixed)






