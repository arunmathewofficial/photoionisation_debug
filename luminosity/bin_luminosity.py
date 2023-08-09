import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd

'''
In each file: col.3=wavelength in nm
              col.4=frequency nu (s^-1)
              col.5=Hnu (erg/cm^2/s/Hz/ster)
              col.6=Hcont (erg/cm^2/s/Hz/ster)
              col.7=Hnu/Hcont
Flambda=4*Hnu*c/wavelength^2  c=light velocity   
'''


files = glob.glob("*.dat")

#Energy bins
bins_left = np.array([7.64, 11.2, 13.6, 16.3, 21.56, 24.6, 30.65, 35.1, 40.96, 47.89, 54.4, 64.5])*2.417989e14
bins_right = np.array([11.2, 13.6, 16.3, 21.56, 24.6, 30.65, 35.1, 40.96, 47.89, 54.4, 64.5, 77])*2.417989e14

for filename in files:
    binned_fluxes = [] #bins to hold all fluxes in appropriate range
    binned_freqs = []
    
    #list to hold integrated flux values
    integrated_fluxes = []
    
    for i in range(len(bins_right)):
        binned_fluxes.append([])
        binned_freqs.append([])
    
    flux = []
    freq = []
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = lines[:-1] #delete last line, which for some reason is just the word Flux
        for line in lines:
            #Pull effective temperature from first line of file
            if "TEFF" in line:
                Teff = float(line[5:13])
                print(Teff)
                continue
            #Ignore the other metadata line
            elif "TITLE" in line:
                continue
            #pull flux and frequency from each data line
            else:
                flx = line[40:54]
                try:
                    base, exponent = flx.split("E")
                    flux.append(float(base + "E" + exponent))
                except:
                    base, exponent = flx.split("-") #catches bad syntax, missing the E
                    flux.append(float(base + "E-" + exponent))
                frq = float(line[26:40])
                freq.append(frq)
    
    #collect up flux/freq pairs within appropriate ranges
    for i in range(len(freq)):
        for j in range(len(bins_right)):
            if freq[i] < bins_right[j] and freq[i] > bins_left[j]:
                binned_fluxes[j].append(flux[i])
                binned_freqs[j].append(freq[i])
                break
    
    #integrate to get total flux within ranges
    for b in range(len(bins_right)):
        int_flux = np.trapz(np.asarray(binned_fluxes[b]), np.asarray(binned_freqs[b]))
        integrated_fluxes.append(int_flux)

    #integrate over entire freq domain to get total flux for normalising
    total_int_flux = np.trapz(np.asarray(flux), np.asarray(freq))
    integrated_fluxes /= total_int_flux
    
    fig = plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex=ax1)
    ax1.set_yscale('log')
    ax2.set_yscale('log')
    ax1.plot(freq, flux)
    ax1.set_ylabel("F(v)")
    ax1.set_title("SED and Integrated Flux, T =" + str(Teff) + "K")
    #ax2.scatter(bins_left, integrated_fluxes, label="Left bin limit")
    #ax2.scatter(bins_right, integrated_fluxes, label="Right bin limit")
    
    ax2.bar(bins_left, integrated_fluxes, align="edge", width= bins_right - bins_left, edgecolor="k")
    ax2.set_ylabel("Binned flux / total flux")
    ax2.set_xlabel("Frequency (Hz)")
    plt.savefig("logbinned_flux"+str(Teff)+".png")
    plt.close()




    luminosity = 3.846e+38 # units ergs/s
    bin_luminosity = luminosity*integrated_fluxes
    data = {"bin_min": bins_left/2.417989e14, "bin_max": bins_right/2.417989e14, "Bin Luminosity": bin_luminosity}
    df = pd.DataFrame(data)
    # Define the path to the CSV file
    csv_file_path = 'bin_luminosity.txt'
    # Write the DataFrame to a CSV file
    df.to_csv(csv_file_path, sep='\t', index=False, float_format='%.5e')
    print(f"DataFrame written to {csv_file_path}")
