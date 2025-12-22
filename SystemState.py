import itertools
import SpatialState
import SpinState
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
