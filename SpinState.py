class SpinState:
    """
    Spin state of a single particle or coupled system.
    """

    spin: float
    m: float
    
    def __init__(self, spin: float, m: float):
        self.spin = spin
        self.m = m

    def getSpin(self) -> float:
        return self.spin
    
    def projection(self) -> float:
        return self.m

    def dimension(self) -> int:
        return int(2 * self.spin + 1)

    def __repr__(self):
        return f"|s={self.spin}, m={self.m}>"
