from cross_section import photo_xsection
import numpy as np
import matplotlib.pyplot as plt
from readpion_mean_xsection import read_data
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# read the xsection data and return label, species name and data dictionary
pion_xsection_data = read_data("/home/tony/Desktop/pion/photoionisation_test/MPV10-photo-tables/mean-photo-xsection.txt")
species = np.array(pion_xsection_data['species'])
# read the weight data and return label, species name and data dictionary
pion_weight_data = read_data("/home/tony/Desktop/pion/photoionisation_test/MPV10-photo-tables/bin-weights.txt")

# Customize the formatting options
np.set_printoptions(threshold=np.inf)
formatted_species_list = np.array2string(species, separator=', ', max_line_width=90)
# Display the formatted string array
print("Found the following species: \n", formatted_species_list)
# obtain minimum and maximum energy from the pion photo-ionisation bin
min_energy = pion_xsection_data["dict"]["Bin_Min"][0]
max_energy = pion_xsection_data["dict"]["Bin_Max"][-1]
# make energy array of 100 points within this limits
energy_array = np.linspace(min_energy, max_energy, 100)
# make histogram energy points
energy_bins = pion_xsection_data["dict"]["Bin_Min"]
#energy_bins.append(max_energy)

print(energy_bins)

for species in pion_xsection_data["species"]:

    species_xsection_array = photo_xsection.get_species_xsection(species, energy_array)
    # multiplying thw weight

    species_xsection_bin = [pion_xsection_data["dict"][species][i] * pion_weight_data['dict'][species][i]
              for i in range(len(pion_xsection_data["dict"][species]))]
    #species_xsection_bin = pion_xsection_data["dict"][species]
    species_xsection_bin_Mb = [x * 1.0E+18 for x in species_xsection_bin]
    nbins = len(species_xsection_bin_Mb)

    y_min = min(species_xsection_bin_Mb)
    y_max = max(species_xsection_bin_Mb)


    # Create a figure with subplots
    fig, ax1 = plt.subplots()

    # Plot the curve
    ax1.plot(energy_array, species_xsection_array, label="Verner-fit", color='black',
             linestyle='-', linewidth=2)
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
    ax2.bar(energy_bins, species_xsection_bin_Mb, width=energy_bins, align='edge', color='orange',
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

