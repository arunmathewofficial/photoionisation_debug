import os
import numpy as np
import matplotlib.pyplot as plt  # importing matplotlib package

m_H = 1.6738e-24
m_He = 6.6464768e-24
m_C = 1.994374e-23
m_N = 2.325892e-23
m_O = 2.6567628e-23
m_Ne = 3.3509177e-23
m_Si = 4.6637066e-23
m_S = 5.3245181e-23
m_Fe = 9.2732796e-23



X_H = 7.35821E-01

a_He = - 1.0
a_C  = - 3.66
a_N  = - 4.40
a_O  = - 3.48
a_Ne = - 4.30
a_Si = - 5.05
#a_S  =
#a_Fe =

def abundance2massfraction(abundance, species_mass, X_H):
    return pow(10, abundance) * species_mass * X_H / m_H

print("mass-fraction He :" + f"{abundance2massfraction(a_He, m_He, X_H):.5E}")
print("mass-fraction C  :" + f"{abundance2massfraction(a_C, m_C, X_H):.5E}")

print("mass-fraction N  :" + f"{abundance2massfraction(a_N, m_N, X_H):.5E}")
print("mass-fraction O  :" + f"{abundance2massfraction(a_O, m_O, X_H):.5E}")
print("mass-fraction Ne :" + f"{abundance2massfraction(a_Ne, m_Ne, X_H):.5E}")
print("mass-fraction Si :" + f"{abundance2massfraction(a_Si, m_Si, X_H):.5E}")