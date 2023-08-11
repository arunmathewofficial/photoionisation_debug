from data import photo_cross_section_data
from data import ionization_threshold
import math
import logging

class photo_xsection:

    def species_xsection(species, E):
        
        xsection_obj = photo_cross_section_data
        fit_emax = xsection_obj.get_xsection_parameters(species).fit_emax
        E0 = xsection_obj.get_xsection_parameters(species).E0
        sigma0 = xsection_obj.get_xsection_parameters(species).sigma0
        ya = xsection_obj.get_xsection_parameters(species).ya
        P = xsection_obj.get_xsection_parameters(species).P
        yw = xsection_obj.get_xsection_parameters(species).yw
        y0 = xsection_obj.get_xsection_parameters(species).y0
        y1 = xsection_obj.get_xsection_parameters(species).y1

        # if E < ionisation_energy: return 0.0
        threshold_obj = ionization_threshold
        Eth = threshold_obj.get_ionisation_energy(species).ionization_energy
        if E < Eth: return 0.0


        if E > fit_emax:
            logging.warning(f"multi-ion photo-xsection: energy exceeds fit range for {species}, E: {E} eV")

        x = E / E0 - y0
        y = math.sqrt(x * x + math.pow(y1, 2.0))
        Fy = (math.pow(x - 1.0, 2.0) + math.pow(yw, 2.0)) * \
             math.pow(y, 0.5 * P - 5.5) * \
             math.pow(1.0 + math.sqrt(y / ya), - P)
        sigmaE = sigma0 * 1e-18 * Fy
        return sigmaE


    def get_species_xsection(species, energy_array):
        xsection_array = []
        for energy in energy_array:
            xsection_array.append(photo_xsection.species_xsection(species, energy))
        xsection_array_Mb = [x * 1.0E+18 for x in xsection_array]
        return xsection_array_Mb








