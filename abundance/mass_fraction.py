import os
import numpy as np
import matplotlib.pyplot as plt  # importing matplotlib package
import pandas as pd
print("This script can be a part of pymicropion")
m_H = 1.6738e-24
m_He = 6.6464768e-24
m_C = 1.994374e-23
m_N = 2.325892e-23
m_O = 2.6567628e-23
m_Ne = 3.3509177e-23
m_Si = 4.6637066e-23
m_S = 5.3245181e-23
m_Fe = 9.2732796e-23

#########################################################
# given data
print("Given density and relative abundance, calculate mass fractions")
# number denisty of hydrogen
rho = 100 * m_H      #in units of g/cm^-3
# relative abundance
a_He = - 1.0
a_C  = - 3.6576
a_N  = - 4.3979
a_O  = - 3.4815
a_Ne = - 4.3010
a_S  = - 5.0458

input = {'Density': [rho], 'a_He': [a_He], 'a_C': [a_C], 'a_N': [a_N], 'a_O': [a_O],
          'a_Ne': [a_Ne], 'a_S': [a_S]}

input_dataframe = pd.DataFrame(input, index=None)
input_dataframe.index = ["" for _ in range(len(input_dataframe))]  # Set empty string labels for the index
print(input_dataframe)
#########################################################

frac_He = 10**a_He
frac_C  = 10**a_C
frac_N  = 10**a_N
frac_O  = 10**a_O
frac_Ne = 10**a_Ne
frac_S  = 10**a_S

# calculating number density of hydrogen.
n_H = rho / (m_H + m_He*frac_He + m_C*frac_C + m_N*frac_N + m_O*frac_O + m_Ne*frac_Ne + m_S*frac_S)
print("Hydrogen number density (in log): ", np.log10(n_H))
n_He = frac_He * n_H
n_C  = frac_C  * n_H
n_N  = frac_N  * n_H
n_O  = frac_O  * n_H
n_Ne = frac_Ne * n_H
n_S  = frac_S  * n_H


print("Calculated Mass-fraction: ")

def massfraction(species_number_density, species_mass, density):
    return species_number_density * species_mass / density

X_H = massfraction(n_H, m_H, rho)
X_He = massfraction(n_He, m_He, rho)
X_C = massfraction(n_C, m_C, rho)
X_N = massfraction(n_N, m_N, rho)
X_O = massfraction(n_O, m_O, rho)
X_Ne = massfraction(n_Ne, m_Ne, rho)
X_S = massfraction(n_S, m_S, rho)

print("mass-fraction H  :" + f"{X_H:.5E}")
print("mass-fraction He :" + f"{X_He:.5E}")
print("mass-fraction C  :" + f"{X_C:.5E}")
print("mass-fraction N  :" + f"{X_N:.5E}")
print("mass-fraction O  :" + f"{X_O:.5E}")
print("mass-fraction Ne :" + f"{X_Ne:.5E}")
print("mass-fraction S  :" + f"{X_S:.5E}")


Sum = X_H + X_He + X_C + X_N + X_O + X_Ne + X_S
print("Sum of Mass fraction:", Sum)

if Sum > 1.0:
    print("Mass fraction exceed 1.0, X :", Sum)