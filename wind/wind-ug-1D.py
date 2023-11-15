# -*- coding: iso-8859-15 -*-

import sys
#sys.path.insert(0,"/home/jm/code/pypion/silo/lib")
#sys.path.insert(0,"/home/jm/code/pypion/Library")
sys.path.insert(0,"/home/mathew/.local/silo/lib/")
#sys.path.insert(0,"/mnt/local/jm/pion_python/src/pypion/")
#sys.path.insert(0,"/home/jmackey/code/pypion/silo/lib")
#sys.path.insert(0,"/home/jmackey/code/pypion/Library")
import Silo
#import Plotting_Classes as ppion
#sys.path.append("/mnt/massive-stars/share/pypion/silo/lib")
#sys.path.append("/mnt/massive-stars/share/pypion/Library")
#import Plotting_Classes as pypion
#from ReadData import ReadData
from pypion.ReadData import ReadData
#from SiloHeader_data import OpenData

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import MultipleLocator
#plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#plt.rc('text', usetex=True)
#plt.rc('font',**{'size': 20})
#plt.rc('lines', linewidth=2)
import argparse
from os import listdir
import glob

import astropy.units as u
from astropy import constants as apc


plt.rcParams["font.weight"] = "normal"
from matplotlib.font_manager import FontProperties

font = FontProperties()
font.set_family('sans-serif')
font.set_name('stixsans')
font.set_style('italic')
font.set_weight('light')
font.set_size(12)

plt.rcParams['font.family'] = 'Times New Roman'

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("fbase", type=str)
parser.add_argument("img_path", type=str)
args = parser.parse_args()
path = args.path
fbase = args.fbase
img_path = args.img_path

mH = 1.6735575e-24 # in gms

files = sorted(glob.glob(path+"/"+fbase+".*.silo"))

for i in range(len(files)):
  print(i,files[i])
  #dataio=OpenData([files[i]])
  dataio = ReadData([files[i]])
  n = dataio.nlevels()
  c = dataio.cycle()
  #print(n,c)
  Density = dataio.get_1Darray("Density")
  rho  = Density['data'][0]
  time = (Density['sim_time'] * u.s).to(u.yr)
  print("Time=",time)
  xmax = (Density['max_extents'] * u.cm).to(u.pc)
  xmin = (Density['min_extents'] * u.cm).to(u.pc)
  ng  = dataio.ngrid()
  dx = (xmax-xmin)/ng
  xmin = xmin[0]
  xmax = xmax[0]
  ng = ng[0]
  dx = dx[0]
  x0 = xmin[0]+0.5*dx[0]
  xn = xmax[0]-0.5*dx[0]
  x = np.linspace(x0,xn,ng)


  vx = dataio.get_1Darray("VelocityX")['data'][0]
  temperature = dataio.get_1Darray("Temperature")['data'][0]


  # chemical species
  # HYDROGEN
  X_H = dataio.get_1Darray("Tr000_X_H")['data'][0]
  H1p = dataio.get_1Darray("Tr009_H1p")['data'][0] / X_H
  H0 = np.ones_like(H1p) - H1p
  # hydrogen number density
  nH = X_H * rho / mH

  # HELIUM
  X_He = dataio.get_1Darray("Tr001_X_He")['data'][0]
  He1p = dataio.get_1Darray("Tr010_He1p")['data'][0] / X_He
  He2p = dataio.get_1Darray("Tr011_He2p")['data'][0] / X_He
  He0 = np.ones_like(X_He) - He1p - He2p
  # Carbon
  X_C = dataio.get_1Darray("Tr002_X_C")['data'][0]
  C1p = dataio.get_1Darray("Tr012_C1p")['data'][0] / X_C
  C2p = dataio.get_1Darray("Tr013_C2p")['data'][0] / X_C
  C3p = dataio.get_1Darray("Tr014_C3p")['data'][0] / X_C
  C4p = dataio.get_1Darray("Tr015_C4p")['data'][0] / X_C
  C5p = dataio.get_1Darray("Tr016_C5p")['data'][0] / X_C
  C6p = dataio.get_1Darray("Tr017_C6p")['data'][0] / X_C
  C0 = np.ones_like(X_C) - C1p - C2p - C3p - C4p - C5p - C6p

  # Nitrogen
  X_N = dataio.get_1Darray("Tr003_X_N")['data'][0]
  N1p = dataio.get_1Darray("Tr018_N1p")['data'][0] / X_N
  N2p = dataio.get_1Darray("Tr019_N2p")['data'][0] / X_N
  N3p = dataio.get_1Darray("Tr020_N3p")['data'][0] / X_N
  N4p = dataio.get_1Darray("Tr021_N4p")['data'][0] / X_N
  N5p = dataio.get_1Darray("Tr022_N5p")['data'][0] / X_N
  N6p = dataio.get_1Darray("Tr023_N6p")['data'][0] / X_N
  N7p = dataio.get_1Darray("Tr024_N7p")['data'][0] / X_N
  N0 = np.ones_like(X_N) - N1p - N2p - N3p - N4p - N5p - N6p - N7p


# plot figures *************************************************************
  fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 6), sharex=True)

  ax1.plot(x, np.log10(vx*10e-6),"C0",label="$ \log \, \left( \mathrm{v_r} / 10 \mathrm{km \, s}^{-1} \\right) $")
  ax1.plot(x, np.log10(temperature*1.0e-5),"C3",label="$ \log \, (\mathrm{T}\, / 10^5\,\mathrm{K})$")
  ax1.plot(x, np.log10(rho*1.0e+24),"g",label=r"$\log \, (\mathrm{\rho} \, / 10^{-24}\, \mathrm{g cm}^{-3})$")
  ax1.plot(x, np.log10(nH),"m--",label=r"$\log \, (\mathrm{n_H} \, / \mathrm{cm}^{-3})$")


  #ax1.set_xlabel('Radius (pc)')
  ax1.set_ylabel('Flow quantities')
  ax1.set_ylim(-4, 4)  # Set the y-limits for the first subplot
  ax1.set_xlim(0.0, 12.5)
  #axs[0].tick_params(labelsize=16)
  #axs[0].grid()
  #axs[0].legend(fontsize=12, loc="lower right")
  ax1.legend(loc='upper left', bbox_to_anchor=(0.035, 0.82), ncol=2,frameon=False)
  s = "$\mathrm{Time}: $" + f"{time:0.02f}"
  ax1.text(9.5, 2.5, s, color="black", fontsize=14)
  ax1.tick_params(axis='both', which='both', direction='in')


  # Hydrogen
  ax2.plot(x, H0,  label="$\mathrm{H}$")
  ax2.plot(x, H1p, label="$\mathrm{H}^{1+}$")
  # Helium
  ax2.plot(x, He0, label="$\mathrm{He}$")
  ax2.plot(x, He1p, label="$\mathrm{He}^{1+}$")
  ax2.plot(x, He2p, label="$\mathrm{He}^{2+}$")
  # Carbon
  ax2.plot(x, C0,  label="$\mathrm{C}$")
  ax2.plot(x, C1p, label="$\mathrm{C}^{1+}$")
  ax2.plot(x, C2p, label="$\mathrm{C}^{2+}$")
  ax2.plot(x, C3p, label="$\mathrm{C}^{3+}$")
  ax2.plot(x, C4p, label="$\mathrm{C}^{4+}$")
  ax2.plot(x, C5p, "--", label="$\mathrm{C}^{5+}$")
  ax2.plot(x, C6p, "--", label="$\mathrm{C}^{6+}$")

  legend1 = ax2.legend(loc='lower left', bbox_to_anchor=(0.03, 0.45), ncol=5, frameon=False)
  plt.gca().add_artist(legend1)

  # Nitrogen
  ax2.plot(x, N0, "--", label="$\mathrm{N}$")
  ax2.plot(x, N1p, "--", label="$\mathrm{N}^{1+}$")
  ax2.plot(x, N2p, "--", label="$\mathrm{N}^{2+}$")
  ax2.plot(x, N3p, "--", label="$\mathrm{N}^{3+}$")
  ax2.plot(x, N4p, "--", label="$\mathrm{N}^{4+}$")
  ax2.plot(x, N5p, "--", label="$\mathrm{N}^{5+}$")
  ax2.plot(x, N6p, "--", label="$\mathrm{N}^{6+}$")
  ax2.plot(x, N7p, "--", label="$\mathrm{N}^{7+}$")



  legend2 = ax2.legend(loc='upper right')

  labels_to_remove = ['$\mathrm{H}$', '$\mathrm{H}^{1+}$', '$\mathrm{He}$', '$\mathrm{He}^{1+}$',
                      '$\mathrm{He}^{2+}$', '$\mathrm{C}$', '$\mathrm{C}^{1+}$', '$\mathrm{C}^{2+}$',
                      "$\mathrm{C}^{3+}$", '$\mathrm{C}^{4+}$', '$\mathrm{C}^{5+}$', '$\mathrm{C}^{6+}$' ]
  # Remove a specific entry (e.g., 'Dataset 1') from the legend and the line
  handles, labels = ax2.get_legend_handles_labels()
  filtered_handles = [handle for handle, label in zip(handles, labels)  if label not in labels_to_remove]
  filtered_labels = [label for label in labels if label not in labels_to_remove]

  ax2.legend(filtered_handles, filtered_labels, loc='lower left', bbox_to_anchor=(0.7, 0.3), ncol=3, frameon=False)

  #plt.gca().add_artist(legend2)


  ax2.set_xlim(0.0, 12.5)
  ax2.set_xlabel('Radius (pc)')
  ax2.set_ylabel('$\mathrm{Ionisation \, Fraction}$')
  #axs[1].grid()
  #ax2.legend(loc='lower left', bbox_to_anchor=(0.15, -0.4), ncol=10)
  ax2.tick_params(axis='both', which='both', direction='in')


# Save images **************************************************************
  x_minor_locator = MultipleLocator(0.2)  # Set the minor tick interval to 0.2 units
  ax1.xaxis.set_minor_locator(x_minor_locator)

  # Define the positions for additional minor ticks on the y-axis
  y_minor_locator = MultipleLocator(1)  # Set the minor tick interval to 0.1 units
  ax1.yaxis.set_minor_locator(y_minor_locator)

  plt.subplots_adjust(hspace=0.1)
  iy = str(i).zfill(5)
  opf = img_path+"/"+fbase+"."+iy+".png"
  plt.savefig(opf, bbox_inches="tight", dpi=300)
  plt.close(fig)
  dataio.close()


  # delete ***************************************************
  del dataio
  del fig
  del X_H, X_He, X_C, X_N
  del H0, H1p
  del He0, He1p, He2p
  del C0, C1p, C2p, C3p, C4p, C5p, C6p
  del N0, N1p, N2p, N3p, N4p, N5p, N6p, N7p
  del Density, vx, temperature, time
  del xmin, xmax, dx, ng, c, n, x, xn, x0


quit()



