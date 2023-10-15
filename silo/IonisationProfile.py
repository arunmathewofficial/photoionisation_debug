
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
    #O1p = object.get_parameter('Tr025_O1p')/object.get_parameter('Tr004_X_O')
    #O2p = object.get_parameter('Tr026_O2p') / object.get_parameter('Tr004_X_O')
    #O3p = object.get_parameter('Tr027_O3p') / object.get_parameter('Tr004_X_O')
    #O4p = object.get_parameter('Tr028_O4p') / object.get_parameter('Tr004_X_O')
    #O5p = object.get_parameter('Tr029_O5p') / object.get_parameter('Tr004_X_O')
    #O6p = object.get_parameter('Tr029_O5p') / object.get_parameter('Tr004_X_O')
    #O0 = np.ones_like(O1p) - O1p - O2p - O3p - O4p - O5p - O6p


    H1p = object.get_parameter('Tr001_H1p')/object.get_parameter('Tr000_X_H')
    H0 = np.ones_like(H1p) - H1p

    radius = object.get_radial_coordinate()


    fig = plt.figure(figsize=(4, 3))
    plots = [H0, H1p]  # Create a new list for each plot
    Plot_Function().Single_Xaxis_Plotter(fig, radius, plots,
                                         ["radius (cm)", r"${\rm T (K)}$"], [])
    #plt.ylim([-15, -5])

    # Saving the plot
    imagefile = "%s%s_%s.png" % (OutputDir, Inputs.img_file, str(imagefile_count).zfill(3))
    plt.savefig(imagefile, bbox_inches='tight', dpi=300)
    print("Saving " + imagefile)
    imagefile_count += 1
    plt.close()
    object.close()

    # ***********************************************************