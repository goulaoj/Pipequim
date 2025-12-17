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
