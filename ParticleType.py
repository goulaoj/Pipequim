from enum import Enum
from math import factorial

class Statistics(Enum):
    BOSON = "boson"
    FERMION = "fermion"

class ParticleType:
    def __init__(self, statistics: Statistics, spin: float):
        self.statistics = statistics
        self.spin = spin

    def is_boson(self) -> bool:
        return self.statistics == Statistics.BOSON

    def is_fermion(self) -> bool:
        return self.statistics == Statistics.FERMION

    def spin_degeneracy(self) -> int:
        """
        2s + 1 = #m
        """
        return int(2 * self.spin + 1)
    def permutation_sign(self, permutation_parity: int) -> int:
        """
        Retorna o signal da permutação no determinante de Slater
        """
        if self.is_boson():
            return 1
        else:
            return (-1) ** permutation_parity

    def symmetrization_normalization(self, N: int) -> float:
        """
        Todas as partículas estão em níveis diferentes
        """
        return 1.0 / (factorial(N) ** 0.5)

    def allows_multiple_occupation(self) -> bool:
        return self.is_boson()

    def __repr__(self) -> str:
        return (
            f"ParticleType(statistics={self.statistics.value}, "
            f"spin={self.spin})"
        )
