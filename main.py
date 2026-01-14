import numpy as np
import matplotlib.pyplot as plt
from HarmonicOscillator import HarmonicOscillator
from ParticleType import ParticleType, Statistics
from SpatialState import SpatialState
from TotalSpinState import TotalSpinState
from SystemState import SystemState
from InfinitePotentialWell import InfinitePotentialWell

Oscillator = HarmonicOscillator()
Well = InfinitePotentialWell(a=1.0)

x = np.linspace(-5, 5, 300)
X1, X2 = np.meshgrid(x, x)

boson = ParticleType(Statistics.BOSON, 0)
fermion = ParticleType(Statistics.FERMION, 0.5)

boson_spinState = TotalSpinState(0, 0.)
fermion_triplet_spinState = TotalSpinState(1, 1)
fermion_singlet_spinState = TotalSpinState(0, 0)

bosonic_state = SystemState(boson, boson_spinState)
fermionic_triplet_state = SystemState(fermion, fermion_triplet_spinState)
fermionic_singlet_state = SystemState(fermion, fermion_singlet_spinState)

bosonic_state.add_particle(SpatialState(1, Well))
fermionic_triplet_state.add_particle(SpatialState(1, Well))
fermionic_singlet_state.add_particle(SpatialState(1, Well))

bosonic_state.add_particle(SpatialState(1, Well))
fermionic_triplet_state.add_particle(SpatialState(2, Well))
fermionic_singlet_state.add_particle(SpatialState(1, Well))


rho_b = bosonic_state.density_grid(X1, X2)
rho_ft = fermionic_triplet_state.density_grid(X1, X2)
rho_fs = fermionic_singlet_state.density_grid(X1, X2)

def plot_density(rho, title):
    plt.figure()
    plt.imshow(rho, extent=[-3, 3, -3, 3], origin="lower")
    plt.colorbar()
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.show()

plot_density(rho_b, "Bosões: densidade conjunta ρ(x1,x2)")
plot_density(rho_ft, "Fermões (triplete): antibunching")
plot_density(rho_fs, "Fermões (singlete): permitido x1=x2")
    