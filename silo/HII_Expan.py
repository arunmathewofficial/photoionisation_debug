
import matplotlib.pyplot as plt
from pypion.argparse_command import InputValues
from SiloReader import GetSiloData
from OneDPlotter import Plot_Function
import numpy as np
import math
import astropy.units as u
Inputs = InputValues()
timeline = Inputs.time_dicts
dimension = Inputs.dimen
OutputDir = Inputs.img_path

recombination_rate = 2.5080e-13 # cm^3/s
n_H = 100 # cm^{-3}
QH = 4.255291e+49
recombination_time = pow(recombination_rate*n_H, -1.0)
one_parsec = 3.086e+18 # cm

def find_largest_jump(arr):
    max_jump_position = None
    max_jump_value = 0
    found = False

    for i in range(1, len(arr)):
        jump = abs(arr[i] - arr[i-1])
        if jump > max_jump_value:
            found= True
            max_jump_value = jump
            max_jump_position = i
    return max_jump_position, found

# calculating the position of ionisation front in each instance
IF_position = []
IF_time = []
plots = []
imagefile_count = 0
for frame in timeline:
    data = timeline[frame]
    object = GetSiloData(data)
    basic_data = object.get_basic_data()
    time = (basic_data['sim_time'] * u.s).to(u.yr)
    Temperature = object.get_parameter('Temperature')
    log_Temperature = np.log10(Temperature)
    radius = object.get_radial_coordinate()
    radius_pc = radius / one_parsec   # radius in parsec

    jump_position, found = find_largest_jump(Temperature)
    if found:
        IF_position.append(radius_pc[jump_position])
        IF_time.append((basic_data['sim_time'] * u.s).value) # in sec
    object.close()

IF_time = np.array(IF_time)
IF_position = np.array(IF_position)

# calculating the corresponding analytical Ionisation front expansion
factor = 3*QH/(4*math.pi*n_H) # interms of parsec
Analytical_IF_position = []
for time in IF_time:
    Analytical_IF_position.append( pow(factor*time, 1/3) / one_parsec)


# plotting
fig = plt.figure(figsize=(8, 6))
plt.plot(IF_time, IF_position, marker='o', linestyle='-', color='b', label='pion-generated')
plt.plot(IF_time, Analytical_IF_position, marker='o', linestyle='-', color='r', label='Analytical')
plt.xlabel(r'$\rm time \, (s)$')
plt.ylabel(r'$\rm Radius \, (pc)$')
plt.text(1e11, 3.5, r'$Q(H) = 4.255291\times10^{49}\, s^{-1}$', horizontalalignment='center', verticalalignment='bottom', color='black')


#plt.xlim([-1, 10])
imagefile = "%s%s.png" % (OutputDir, Inputs.img_file)
plt.grid()
plt.legend()
plt.savefig(imagefile, bbox_inches='tight', dpi=300)
print("Saving " + imagefile)
plt.close()


