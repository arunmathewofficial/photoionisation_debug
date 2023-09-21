
import matplotlib.pyplot as plt
from pypion.argparse_command import InputValues
from SiloReader import GetSiloData
from OneDPlotter import Plot_Function
import numpy as np

Inputs = InputValues()
timeline = Inputs.time_dicts
dimension = Inputs.dimen
OutputDir = Inputs.img_path

plots = []
imagefile_count = 0
for frame in timeline:
    data = timeline[frame]
    object = GetSiloData(data)
    basic_data = object.get_basic_data()

    # density = object.get_parameter('Density')
    Temperature = object.get_parameter('Temperature')
    log_Temperature = np.log10(Temperature)
    radius = object.get_radial_coordinate()


    fig = plt.figure(figsize=(4, 3))
    plots = [Temperature]  # Create a new list for each plot
    Plot_Function().Single_Xaxis_Plotter(fig, radius, plots,
                                         ["radius (cm)", r"${\rm T (K)}$"], [])
    #plt.ylim([-15, -5])
    plt.ylim([0.0, 20000])
    # Saving the plot
    imagefile = "%s%s_%s.png" % (OutputDir, Inputs.img_file, str(imagefile_count).zfill(3))
    plt.savefig(imagefile, bbox_inches='tight', dpi=300)
    print("Saving " + imagefile)
    imagefile_count += 1
    plt.close()
    object.close()

    # ***********************************************************






'''
import astropy.units as u
import pandas as pd
import numpy as np

#############################################################
# styles
plt.rcParams["font.weight"] = "normal"
from matplotlib.font_manager import FontProperties

font = FontProperties()
font.set_family('sans-serif')
font.set_name('stixsans')
font.set_style('italic')
font.set_weight('light')
font.set_size(12)

#############################################################
# get inputs from argparse
Inputs = InputValues()
timeline = Inputs.time_dicts
dimension = Inputs.dimen

#############################################################
print('*************** PYPION TOOLKIT : THERMO PLOTTER *****************')
# Exit if not 1D data
if dimension == "1D":
    print('Plotting 1D silo data ...')
else:
    print('Not 1D data, exiting ...')
    quit()

#############################################################
# Making Output directory
# If already exist, the pass.
OutputDir = Inputs.img_path
# Create target Directory
try:
    os.mkdir(OutputDir)
    print("Output directory:", OutputDir, "created.")
except FileExistsError:\
    print("Output directory", OutputDir, "already exists.")
pass


# Mian #############################################################
x_info = ['x', None]
AxisLabel = [r'log(T) K', 'ion fraction']

thermo_list = []
thermo_namelist = []
norm_factor = []

# Thermodynamics quantities
thermo_list_1 = ["Density"]
thermo_namelist_1 = [r"$\rm \rho \, (10^{-23} \, g/cm^3)$"]
norm_factor_1 = 1.0E-23
thermo_list_2 = ['VelocityX']
thermo_namelist_2 = [r"$\rm |v_x| \, (10^2 \, km/s)$"]
norm_factor_2 = 1.0E+7
thermo_list_3 = ["Temperature"]
thermo_namelist_3 = [r"$\rm T \, (10^{5} \, K)$"]
norm_factor_3 = 1.0E+05

plot_name = '_thermo'
thermo_list.append(thermo_list_1)
thermo_namelist.append(thermo_namelist_1)
norm_factor.append(norm_factor_1)
thermo_list.append(thermo_list_2)
thermo_namelist.append(thermo_namelist_2)
norm_factor.append(norm_factor_2)
thermo_list.append(thermo_list_3)
thermo_namelist.append(thermo_namelist_3)
norm_factor.append(norm_factor_3)

# Figure parameters ############################################################
fig_rows = 3 # number of rows in the figure
fig_cols = 1 # number of cols in the figure
#xlimit = [0, 2e+20] # limit x range of the plot with this interval, empty = default
xlimit = [] # limit x range of the plot with this interval, empty = default
ylimit = [] # limit y range of the plot with this interval, empty = default
resolution = 300 # control the resolution of the output image
figsize = (3,4) # set the size of the image, set to 'None' for default
axislabel = ['x (cm)', 'ionisation fraction'] # axis labels
split = []
print2file = True
plot_info = [fig_rows, fig_cols, xlimit, ylimit, figsize, axislabel, split, print2file]


imagefile_count = 0
# Call OneDGrid_Advanced_Plotter for every time instant
for frame in timeline:
    data = timeline[frame]
    silo_plot = Silo_Plotter(data)
    output = silo_plot.OneDGrid_Advanced_Plotter(x_info, thermo_list, thermo_namelist, norm_factor, plot_info)
    print('[Time {:.2e}]'.format(output['time']), 'Saving image:' + str(imagefile_count).zfill(4))
    imagefile = "%s%s%s_%s.png" % (OutputDir, Inputs.img_file, plot_name, str(imagefile_count).zfill(3))

    if print2file == True:
        textfile = "%s%s%s_%s.txt" % (OutputDir, Inputs.img_file, plot_name, str(imagefile_count).zfill(3))
        table = pd.DataFrame(output['data'])
        table.to_csv(textfile, float_format='%.5e')


    plt.savefig(imagefile, bbox_inches='tight', dpi=resolution)
    imagefile_count += 1
    plt.close()
    silo_plot.close()

print('*************** PYPION TOOLKIT : THERMO PLOTTER *****************')
'''