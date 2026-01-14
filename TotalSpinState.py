class TotalSpinState:
    """
    Spin state of a single particle or coupled system.
    """

    S: float
    m: float
    
    def __init__(self, S: float, m: float):
        self.S = S
        self.m = m
    
    def projection(self) -> float:
        return self.m 

    def dimension(self) -> int:
        return int(2 * self.S + 1)
    
    def is_singlet(self) -> bool:
        return self.S == 0

    def is_triplet(self) -> bool:
        return self.S == 1

    def __repr__(self):
        return f"|s={self.S}, m={self.m}>"
