import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from HarmonicOscillator import HarmonicOscillator
from ParticleType import ParticleType, Statistics
from SpatialState import SpatialState
from TotalSpinState import TotalSpinState
from SystemState import SystemState
from InfinitePotentialWell import InfinitePotentialWell

# --------- Configuração do Sistema ---------

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

bosonic_state.add_particle(SpatialState(0, Oscillator))
fermionic_triplet_state.add_particle(SpatialState(0, Oscillator))
fermionic_singlet_state.add_particle(SpatialState(0, Oscillator))

bosonic_state.add_particle(SpatialState(0, Oscillator))
fermionic_triplet_state.add_particle(SpatialState(0, Oscillator))
fermionic_singlet_state.add_particle(SpatialState(0, Oscillator))


# --------- Cálculo das densidades conjuntas e funções de correlação ---------
rho_b = bosonic_state.density_grid(X1, X2)
rho_ft = fermionic_triplet_state.density_grid(X1, X2)
rho_fs = fermionic_singlet_state.density_grid(X1, X2)

unsym_rho = bosonic_state.unsym_density_grid(X1, X2)
unsym_g2 = bosonic_state.unsym_correlation_function_grid(X1, X2)

g2_b  = bosonic_state.correlation_function_grid(X1, X2)
g2_ft = fermionic_triplet_state.correlation_function_grid(X1, X2)
g2_fs = fermionic_singlet_state.correlation_function_grid(X1, X2)

# --------- Plots ---------

def plot_density(rho, x, title):
    plt.figure()
    plt.imshow(rho, extent=[x.min(), x.max(), x.min(), x.max()], origin="lower")
    plt.colorbar()
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.show()

def plot_density_3D(X1, X2, rho, title):
   
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(
        X1, X2, rho, 
        cmap='viridis', edgecolor='none',
        alpha = 0.9
    )
    
    cbar = fig.colorbar(surf, shrink=0.6, aspect=10)
    cbar.set_label(r"$\rho(x_1,x_2)$")

    ax.set_xlabel(r"$x_1$")
    ax.set_ylabel(r"$x_2$")
    ax.set_zlabel(r"$\rho$")
    ax.set_title(title)

    plt.tight_layout()
    plt.show()
    
def plot_correlation_g2(g2, x, title):
    
    plt.figure()
    plt.imshow(g2, extent=[x.min(), x.max(), x.min(), x.max()], origin="lower")
    plt.colorbar()
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.title(title)
    plt.show()
    
# Simetrizado   
# plot_density(rho_b, x, "Bosões: densidade conjunta ρ(x1,x2)")
# plot_density(rho_ft, x, "Fermões (triplete): antibunching")
# plot_density(rho_fs, x, "Fermões (singlete): permitido x1=x2")

# Não simetrizado (tipo de particula indiferente)
plot_density(unsym_rho, x, "Partículas Distinguíveis: ρ(x1,x2)")
plot_correlation_g2(unsym_g2, x, "Partículas Distinguíveis: g²(x1,x2)")

# 3D
# plot_density_3D(X1, X2, rho_b, "Bosões: densidade conjunta ρ(x1,x2)")
# plot_density_3D(X1, X2, rho_ft, "Fermões (triplete): antibunching")
# plot_density_3D(X1, X2, rho_fs, "Fermões (singlete): permitido x1=x2")

# Função de correlação g2
# plot_correlation_g2(g2_b, x, "Bosões: função de correlação g²(x1,x2)")
# plot_correlation_g2(g2_ft, x, "Fermões (triplete): função de correlação g²(x1,x2)")
# plot_correlation_g2(g2_fs, x, "Fermões (singlete): função de correlação g²(x1,x2)")


# --------- Cálculo de valores esperados ---------

# # <x1^2>
# def op_x1_squared(X1, X2): 
#     return X1**2

# # <x1 x2>
# def op_x1_x2(X1, X2):
#     return X1 * X2

# # <(x1 - x2)^2>
# def op_dx_squared(X1, X2):
#     return (X1 - X2)**2 

# print("Bosões:")
# print("⟨x1^2⟩ =", bosonic_state.expectation(op_x1_squared, X1, X2))
# print("⟨x1 x2⟩ =", bosonic_state.expectation(op_x1_x2, X1, X2))
# print("⟨(x1-x2)^2⟩ =", bosonic_state.expectation(op_dx_squared, X1, X2))

# print("\nFermiões triplete:")
# print("⟨x1^2⟩ =", fermionic_triplet_state.expectation(op_x1_squared, X1, X2))
# print("⟨x1 x2⟩ =", fermionic_triplet_state.expectation(op_x1_x2, X1, X2))
# print("⟨(x1-x2)^2⟩ =", fermionic_triplet_state.expectation(op_dx_squared, X1, X2))

# print("\nFermiões singlete:")
# print("⟨x1^2⟩ =", fermionic_singlet_state.expectation(op_x1_squared, X1, X2))
# print("⟨x1 x2⟩ =", fermionic_singlet_state.expectation(op_x1_x2, X1, X2))
# print("⟨(x1-x2)^2⟩ =", fermionic_singlet_state.expectation(op_dx_squared, X1, X2))