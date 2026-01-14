import numpy as np
from math import factorial, sqrt, pi
from scipy.special import hermite

class HarmonicOscillator:
    
    
    def energy(self, n: int) -> float:
        """
        Consideramos o resto das constantes 1
        """
        return n + 0.5
    
    def wavefunction(self, n: int, x: np.ndarray) -> np.ndarray:
        Hn = hermite(n)
        norm = 1.0 / sqrt((2 ** n) * factorial(n) * sqrt(pi))
        return norm * Hn(x) * np.exp(-0.5 * x ** 2)
    