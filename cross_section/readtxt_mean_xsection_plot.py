import numpy as np
import matplotlib.pyplot as plt

# Read the text file
with open('/home/mathew/Desktop/pion/photo_ionisation/MPV10-photo-xsec-table/mean-photo-xsection.txt', 'r') as file:
    lines = file.readlines()

# Extract the labels and data
labels = lines[1].split()[1:]
data = np.genfromtxt(lines[2:], delimiter=' ', usecols=range(2, len(labels) + 2))

# Plotting a separate histogram for each species
for i in range(len(labels)):
    species = labels[i]
    species_data = data[:, i]

    # Plot histogram
    plt.figure()
    plt.hist(species_data, bins=50, color='skyblue', edgecolor='black')
    plt.xlabel('Cross-section (Mb)')
    plt.ylabel('Frequency')
    plt.title(f'Histogram for {species}')
    plt.grid(True)

    # Save the plot
    plt.savefig(f'histogram_{species}.png')

    # Display the plot
    plt.show()
