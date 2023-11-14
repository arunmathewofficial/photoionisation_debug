import math
import numpy
import numpy as np

sigma = 5.6704E-5  # units gs-3K-4
R_sun = 6.9599E+10 # cm

def stefan_luminosity(T_eff, R_star, what_scale):
    if what_scale == 'log':
        return numpy.log10(4*math.pi* pow(R_star, 2.0) *pow(R_sun, 2.0) * sigma * pow(T_eff, 4.0))
    else:
        return 4 * math.pi * pow(R_star, 2.0) * pow(R_sun, 2.0) * sigma * pow(T_eff, 4.0)



T_eff = 40000
R_star= 18.67
print(f'T = {T_eff} K, Radius = {R_star} R_sun')
Lumi = stefan_luminosity(T_eff, R_star,'None')
print(f'L = {Lumi} ergs/s')
print(f'log L = {np.log10(Lumi)}')
