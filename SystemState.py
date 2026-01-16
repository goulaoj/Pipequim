import itertools
from ParticleType import ParticleType, Statistics
from SpatialState import SpatialState
from TotalSpinState import TotalSpinState
import numpy as np

class SystemState:
    """
    Many-body quantum state of identical particles.
    """

    def __init__(self, particle_type, SpinState: TotalSpinState):
        self.particle_type = particle_type
        self.spatial_states = []
        self.total_spin_state = SpinState

        
    def add_particle(self, spatial_state: SpatialState):
        self.spatial_states.append(spatial_state)

    def number_of_particles(self) -> int:
        return len(self.spatial_states)

    def total_energy(self) -> float:
        return sum(state.energy() for state in self.spatial_states)
    
    def required_spatial_symmetry(self):
        """
        Returns +1 (symmetric) or -1 (antisymmetric)
        """
        if self.particle_type.is_boson():
            return +1


        if self.total_spin_state.is_triplet():
            return -1  
        else:
            return +1 


    def symmetrized_spatial_state(self):
        """
        General symmetrized / antisymmetrized state for N particles.

        WARNING: factorial complexity, usable only for small N.
        """
        N = self.number_of_particles()

        if N == 0:
            raise ValueError("Empty system.")

        norm = self.particle_type.symmetrization_normalization(N)

        # Single-particle states
        symmetry = self.required_spatial_symmetry()
        symmetrized_terms = []

        for perm in itertools.permutations(range(N)):
            # Permutation parity
            parity = self._permutation_parity(perm)

            sign = 1
            if symmetry == -1:
                sign = (-1) ** parity

            permuted = [self.spatial_states[i] for i in perm]

            symmetrized_terms.append((sign, permuted))

        return norm, symmetrized_terms

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
    
    def wavefunction(self, positions: np.ndarray) -> np.ndarray:

        positions = np.asarray(positions) 
        
        N = self.number_of_particles()
        if positions.shape[0] != N:
            raise ValueError("Number of positions must match number of particles.")

        norm, sym_terms = self.symmetrized_spatial_state()
        total_wavefunction = 0.0

        for sign, states in sym_terms:
            
            term_wavefunction = 1.0
            
            for i in range(N):
                term_wavefunction *= states[i].wavefunction(positions[i])
            total_wavefunction += sign * term_wavefunction

        return norm * total_wavefunction
    
    def density (self, xs):
        
        psi= self.wavefunction(xs)
        return np.abs(psi)**2
    
    def density_grid(self, X1, X2):
        
        rho = np.zeros_like(X1)

        for i in range(X1.shape[0]):
            
            for j in range(X1.shape[1]):
                
                rho[i, j] = self.density([X1[i, j], X2[i, j]])

        return rho
    
    def one_particle_density(self, rho, x):
        
        dx =  x[1] - x[0]
        return np.trapezoid(rho, dx=dx, axis=1)
    
    
    def correlation_function_grid(self, X1, X2):

        rho = self.density_grid(X1, X2)
        
        rho1_x1 = self.one_particle_density(rho, X1[0,:])
        rho1_x2 = self.one_particle_density(rho, X2[:,0])
        

        rho1_x1 = rho1_x1 / (np.max(rho1_x1) + 1e-12)
        rho1_x2 = rho1_x2 / (np.max(rho1_x2) +1e-12)
        

        rho1_x1_2d = rho1_x1[:, np.newaxis]
        rho1_x2_2d = rho1_x2[np.newaxis, :]
        
        g2 = rho / (rho1_x1_2d * rho1_x2_2d + 1e-12) 
        return g2
    
    def expectation(self, operator, X1, X2):

        rho = self.density_grid(X1, X2)
        
        dx = X1[0,1] - X1[0,0] 
        dy = X2[1,0] - X2[0,0]
        
        op_vals = operator(X1, X2)
        
        expectation_value = np.sum(op_vals * rho) * dx * dy
        return expectation_value

