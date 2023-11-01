# -*- coding: iso-8859-15 -*-

import sys
#sys.path.insert(0,"/home/jm/code/pypion/silo/lib")
#sys.path.insert(0,"/home/jm/code/pypion/Library")
sys.path.insert(0,"/home/tony/.local/silo/lib/")
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

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
parser.add_argument("fbase", type=str)
parser.add_argument("img_path", type=str)
args = parser.parse_args()
path = args.path
fbase = args.fbase
img_path = args.img_path

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
  print("time=",time)
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
  fig, axs = plt.subplots(2, 1, figsize=(12, 8))

  axs[0].plot(x, np.log10(vx*10e-6),"b",label="$v_r\, \left(10 \, \mathrm{km\,s}^{-1}\\right)$")
  axs[0].plot(x, np.log10(temperature*1.0e-5),"r",label="$T\, (10^5\,\mathrm{K})$")
  axs[0].plot(x, np.log10(rho*1.0e+22),"g",label=r"$\rho \, (10^{-22}\,g/cm^3)$")

  axs[0].set_xlabel('Radius (pc)')
  axs[0].set_ylabel('Flow quantities')
  axs[0].set_ylim(-4, 4)  # Set the y-limits for the first subplot
  axs[0].set_xlim(-1, 20)
  #axs[0].tick_params(labelsize=16)
  axs[0].grid()
  #axs[0].legend(fontsize=12, loc="lower right")
  axs[0].legend(loc='upper left', bbox_to_anchor=(0.5, 1.15), ncol=10)
  s = "$\mathrm{time} = $" + f"{time:0.03f}"
  axs[0].text(0.3, 4.3, s, color="black", fontsize=14)

  # Hydrogen
  axs[1].plot(x, H0,  label="$\mathrm{H}$")
  axs[1].plot(x, H1p, label="$\mathrm{H}^{1+}$")
  # Helium
  axs[1].plot(x, He0, label="$\mathrm{He}$")
  axs[1].plot(x, He1p, label="$\mathrm{He}^{1+}$")
  axs[1].plot(x, He2p, label="$\mathrm{He}^{2+}$")
  # Carbon
  axs[1].plot(x, C0,  label="$\mathrm{C}$")
  axs[1].plot(x, C1p, label="$\mathrm{C}^{1+}$")
  axs[1].plot(x, C2p, label="$\mathrm{C}^{2+}$")
  axs[1].plot(x, C3p, label="$\mathrm{C}^{3+}$")
  axs[1].plot(x, C4p, label="$\mathrm{C}^{4+}$")
  axs[1].plot(x, C5p, "--", label="$\mathrm{C}^{5+}$")
  axs[1].plot(x, C6p, "--", label="$\mathrm{C}^{6+}$")
  # Nitrogen
  axs[1].plot(x, N0,  "--", label="$\mathrm{N}$")
  axs[1].plot(x, N1p, "--", label="$\mathrm{N}^{1+}$")
  axs[1].plot(x, N2p, "--", label="$\mathrm{N}^{2+}$")
  axs[1].plot(x, N3p, "--", label="$\mathrm{N}^{3+}$")
  axs[1].plot(x, N4p, "--", label="$\mathrm{N}^{4+}$")
  axs[1].plot(x, N5p, "--", label="$\mathrm{N}^{5+}$")
  axs[1].plot(x, N6p, "--", label="$\mathrm{N}^{6+}$")
  axs[1].plot(x, N7p, "--", label="$\mathrm{N}^{7+}$")

  axs[1].set_xlim(-1, 20)
  axs[1].set_xlabel('Radius (pc)')
  axs[1].set_ylabel('Ionisation Fraction')
  axs[1].grid()
  axs[1].legend(loc='lower left', bbox_to_anchor=(0.0, -0.4), ncol=10)


# Save images **************************************************************
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



