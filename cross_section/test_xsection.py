from cross_section import photo_xsection
import numpy as np
import matplotlib.pyplot as plt
from readpion_mean_xsection import read_data
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# read the xsection data and return label, species name and data dictionary
pion_data = read_data("/home/tony/Desktop/pion/photoionisation_test/MPV10-photo-tables/mean-photo-xsection.txt")
species = np.array(pion_data['species'])
# Customize the formatting options
np.set_printoptions(threshold=np.inf)
formatted_species_list = np.array2string(species, separator=', ', max_line_width=90)
# Display the formatted string array
print("Found the following species: \n", formatted_species_list)
# obtain minimum and maximum energy from the pion photo-ionisation bin
min_energy = pion_data["dict"]["Bin_Min"][0]
max_energy = pion_data["dict"]["Bin_Max"][-1]
# make energy array of 100 points within this limits
energy_array = np.linspace(min_energy, max_energy, 100)
# make histogram energy points
energy_bins = pion_data["dict"]["Bin_Min"]
#energy_bins.append(max_energy)


for species in pion_data["species"]:

    species_xsection_array = photo_xsection.get_species_xsection(species, energy_array)
    species_xsection_bin = pion_data["dict"][species]
    species_xsection_bin_Mb = [x * 1.0E+18 for x in species_xsection_bin]
    nbins = len(species_xsection_bin_Mb)

    y_min = min(species_xsection_bin_Mb)
    y_max = max(species_xsection_bin_Mb)


    # Create a figure with subplots
    fig, ax1 = plt.subplots()

    # Plot the curve
    ax1.plot(energy_array, species_xsection_array, label="Verner-fit", color='red',
             linestyle='--', linewidth=2)
    ax1.set_xlabel("Energy, eV")
    ax1.set_ylabel("Verner Cross section, Mb")
    ax1.set_title('Cross-section for ' + species)
    ax1.xaxis.set_minor_locator(AutoMinorLocator())
    ax1.yaxis.set_minor_locator(AutoMinorLocator())
    ax1.tick_params(axis="both", direction="in", which="both", bottom=True, top=True,
                   left=True, right=True, length=3)
    ax1.legend(loc='upper left')
    ax1.set_ylim(y_min, y_max)

    # Creating a twin axis sharing the x-axis
    ax2 = ax1.twinx()

    # Plot the bar
    #ax2.hist(species_xsection_bin_Mb, bins=nbins, color='blue', alpha=0.7, label='Histogram')
    ax2.bar(energy_bins, species_xsection_bin_Mb, width=3, align='edge', color='orange',
            alpha=0.5, label="MPv10-PION")
    ax2.set_xlabel("Energy, eV")
    ax2.set_ylabel("MPV10 Cross section, Mb")
    ax2.xaxis.set_minor_locator(AutoMinorLocator())
    ax2.yaxis.set_minor_locator(AutoMinorLocator())
    ax2.legend(loc='upper right')
    ax2.set_ylim(y_min, y_max)


    plt.tight_layout()  # To prevent overlapping of subplots
    # Show the combined plot
    image = "/home/tony/Desktop/pion/photoionisation_test/debug_plots/xsection_" + species + ".png"
    print("saving " + image)
    plt.savefig(image, dpi=200)
    plt.close(fig)

'''
# Generate some example data
x_curve = np.linspace(0, 10, 100)
y_curve = np.sin(x_curve)

data_histogram = np.random.normal(0, 1, 1000)  # Example histogram data



# Plot the curve
ax1.plot(x_curve, y_curve, label="Curve")
ax1.set_title("Curve Plot")
ax1.legend()

# Plot the histogram
ax2.hist(data_histogram, bins=20, color='blue', alpha=0.7)
ax2.set_title("Histogram")
ax2.set_xlabel("Values")
ax2.set_ylabel("Frequency")

plt.tight_layout()  # To prevent overlapping of subplots

# Show the combined plot
plt.show()



#
energy_values = np.linspace(12, 33, 100)
xsection_values = photo_xsection.get_species_xsection("C", energy_values)

plt.plot(energy_values, xsection_values, linestyle='-', color='b')
plt.xlabel('Energy, eV')
plt.ylabel('Cross Section, Mb')
plt.tight_layout()
plt.show()

'''
