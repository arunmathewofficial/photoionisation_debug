import matplotlib.pyplot as plt

# Data
energy_bins = [11.0, 13.0, 15.0, 17.0, 19.0, 21.0, 23.0, 25.0, 27.0, 29.0, 31.0, 33.0, 35.0]
mean_cross_sections = [18.064911987442922, 16.057797818488556, 13.959456061881463, 12.078716652000756,
                       10.474332081796472, 9.127674022943332, 8.00080002995195, 7.055376266326382,
                       6.2581281726383375, 5.581706044626461, 5.004103911488793, 4.5077391961635715,
                       4.0785656576481175]

# Plotting the histogram
plt.bar(energy_bins, mean_cross_sections, width=1, align='edge')
plt.xlabel('Energy Bins')
plt.ylabel('Mean Cross-Section for C')
plt.title('Histogram of Mean Cross-Sections for Energy Bins')
#plt.show()
plt.savefig('mean_cross_sections.png')