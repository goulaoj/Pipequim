from HarmonicOscillator import HarmonicOscillator
from InfinitePotentialWell import InfinitePotentialWell

class SpatialState:
    """
    Spatial eigenstate of a single particle.
    """

    def __init__(self, n: int, potential):
        self.n = n
        self.potential = potential
        
    def energy(self) -> float:
        return self.potential.energy(self.n)

    def wavefunction(self, x):
        return self.potential.wavefunction(self.n, x)

    def density(self, x):
        psi = self.wavefunction(x)
        return abs(psi) ** 2
