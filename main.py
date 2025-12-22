import numpy as np
import matplotlib.pyplot as plt
from HarmonicOscillator import HarmonicOscillator
from ParticleType import ParticleType, Statistics
from SpatialState import SpatialState
from SpinState import SpinState
from SystemState import SystemState

Oscillator = HarmonicOscillator()

x = np.linspace(-3, 3, 300)
X1, X2 = np.meshgrid(x, x)

boson = ParticleType(Statistics.BOSON, 0)
fermion = ParticleType(Statistics.FERMION, 0.5)

bosonic_state = SystemState(boson)
fermionic_triplet_state = SystemState(fermion)
fermionic_singlet_state = SystemState(fermion)

bosonic_state.add_particle(SpatialState(0, Oscillator),SpinState(0, 0))
fermionic_triplet_state.add_particle(SpatialState(0, Oscillator),SpinState(0.5, 0.5))
fermionic_singlet_state.add_particle(SpatialState(0, Oscillator),SpinState(0.5, 0.5))

bosonic_state.add_particle(SpatialState(0, Oscillator),SpinState(0, 0))
fermionic_triplet_state.add_particle(SpatialState(0, Oscillator),SpinState(0.5, 0.5))
fermionic_singlet_state.add_particle(SpatialState(0, Oscillator),SpinState(0.5, -0.5))


rho_b = bosonic_state.joint_density(X1, X2)
rho_ft = fermionic_triplet_state.joint_density(X1, X2)
rho_fs = fermionic_singlet_state.joint_density(X1, X2)

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
    