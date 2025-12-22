import itertools
import SpatialState
import SpinState
import numpy as np

class SystemState:
    """
    Many-body quantum state of identical particles.
    """

    def __init__(self, particle_type):
        self.particle_type = particle_type
        self.spatial_states = []
        self.spin_states = []

    def add_particle(self, spatial_state: SpatialState, spin_state: SpinState):
        self.spatial_states.append(spatial_state)
        self.spin_states.append(spin_state)

    def number_of_particles(self) -> int:
        return len(self.spatial_states)

    def total_energy(self) -> float:
        return sum(state.energy() for state in self.spatial_states)

    def single_particle_state(self, index):
        """
        Returns the (SpatialState, SpinState) of particle index.
        """
        return self.spatial_states[index], self.spin_states[index]

    def symmetrized_state(self):
        """
        General symmetrized / antisymmetrized state for N particles.

        WARNING: factorial complexity, usable only for small N.
        """
        N = self.number_of_particles()

        if N == 0:
            raise ValueError("Empty system.")

        norm = self.particle_type.symmetrization_normalization(N)

        # Single-particle states
        single_states = list(zip(self.spatial_states, self.spin_states))

        symmetrized_terms = []

        for perm in itertools.permutations(range(N)):
            # Permutation parity
            parity = self._permutation_parity(perm)

            sign = self.particle_type.permutation_sign(parity)

            permuted_state = tuple(single_states[i] for i in perm)

            symmetrized_terms.append((sign, permuted_state))

        return {
            "normalization": norm,
            "terms": symmetrized_terms
        }

    def _permutation_parity(self, perm):
        """
        Computes parity of a permutation.
        Returns 0 for even, 1 for odd.
        """
        perm = list(perm)
        visited = [False] * len(perm)
        parity = 0

        for i in range(len(perm)):
            if visited[i]:
                continue
            cycle_length = 0
            j = i
            while not visited[j]:
                visited[j] = True
                j = perm[j]
                cycle_length += 1
            if cycle_length > 0:
                parity += cycle_length - 1

        return parity % 2
    
    def joint_density(self, x1, x2):
        """
        Computes the joint spatial density ρ(x1, x2)
        for N = 2 particles, tracing over spin.
        """
        N = self.number_of_particles()
        if N != 2:
            raise NotImplementedError("Joint density implemented only for N = 2.")

        sym_state = self.symmetrized_state()
        norm = sym_state["normalization"]
        terms = sym_state["terms"]

        psi_total = 0.0

        for sign, term in terms:
            (sp_a, spin_a), (sp_b, spin_b) = term

            # Spatial wavefunctions
            psi_a_x1 = sp_a.wavefunction(x1)
            psi_b_x2 = sp_b.wavefunction(x2)

            psi_term = psi_a_x1 * psi_b_x2

            # Spin overlap: ⟨χ|χ⟩ = 1 if same spin, else 0
            spin_factor = 1.0 if spin_a.m == spin_b.m else 0.0

            psi_total += sign * spin_factor * psi_term

        psi_total *= norm
        return np.abs(psi_total) ** 2

    def slater_wavefunction(self, x_values):
        """
        Computes the Slater determinant wavefunction for fermions.

        Parameters
        ----------
        x_values : list or array
            Positions [x1, x2, ..., xN]
        """
        if not self.particle_type.is_fermion():
            raise ValueError("Slater determinant only valid for fermions.")

        N = self.number_of_particles()
        if len(x_values) != N:
            raise ValueError("Number of positions must match number of particles.")

        # Build Slater matrix
        slater_matrix = np.zeros((N, N), dtype=complex)

        for i in range(N):
            for j in range(N):
                sp = self.spatial_states[i]
                spin = self.spin_states[i]

                # Spin part: orthonormal basis
                spin_factor = 1.0  # assuming orthonormal spin states

                slater_matrix[i, j] = (
                    sp.wavefunction(x_values[j]) * spin_factor
                )

        # Determinant
        psi = np.linalg.det(slater_matrix)
        psi /= np.sqrt(np.math.factorial(N))
        return psi

    def one_body_density_slater(self, x):
        """
        One-body density for a fermionic Slater state.
        """
        if not self.particle_type.is_fermion():
            raise ValueError("Only for fermions.")

        rho = 0.0
        for sp in self.spatial_states:
            rho += np.abs(sp.wavefunction(x)) ** 2
        return rho
    
