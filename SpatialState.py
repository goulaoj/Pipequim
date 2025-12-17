class SpatialState:
    """
    Spatial eigenstate of a single particle.
    """

    def __init__(self, n: int, oscillator: HarmonicOscillator):
        self.n = n
        self.oscillator = oscillator
        
    def energy(self) -> float:
        return self.oscillator.energy(self.n)

    def wavefunction(self, x):
        return self.oscillator.wavefunction(self.n, x)

    def density(self, x):
        psi = self.wavefunction(x)
        return abs(psi) ** 2
