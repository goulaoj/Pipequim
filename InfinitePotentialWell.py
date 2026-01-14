import numpy as np
from math import sin, sqrt, pi

class InfinitePotentialWell:
    
    def __init__(self, a: float):
        self.a = a
    
    def energy(self, n: int) -> float:
        """
        Consideramos o resto das constantes 1
        """
        return pi*pi*n*n/(2*self.a*self.a)
    
    def wavefunction(self, n: int, x: np.ndarray):

        return sqrt(2 / self.a) * sin(n * x * pi / self.a)
    