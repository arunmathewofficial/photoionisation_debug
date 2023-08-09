from cross_section import photo_xsection
import numpy as np
import matplotlib.pyplot as plt

energy_values = np.linspace(12, 33, 100)
xsection_values = photo_xsection.get_species_xsection("C", energy_values)

plt.plot(energy_values, xsection_values, linestyle='-', color='b')
plt.xlabel('Energy, eV')
plt.ylabel('Cross Section, Mb')
plt.tight_layout()
plt.show()


