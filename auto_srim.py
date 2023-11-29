# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:17:30 2023

@author: rnv
"""


import os
import ray

from srim import TRIM, Ion
from human_format import human_format


###Fonction Srim
@ray.remote
def auto_srim(ion_implant,cible,nb_ion,tilt,energy,target,calc_method,srim_dir,save_dir):
    """


    Parameters
    ----------
    ion_implant : str
        which ion to implant
    cible : str
        Name of the layers
    nb_ion : int float
        how many ion to run sim
    tilt : float
        which angle
    width : flaot
        width of the layer/s
    nrj : float
        energy of implant

    Returns
    -------
    mainoutput_directory : TYPE
        DESCRIPTION.

    """
    ion = Ion(ion_implant, energy)

    trim = TRIM(target, ion, number_ions=nb_ion, calculation=calc_method, angle_ions=tilt)

    trim.run(srim_dir)

    nrj_km = human_format(energy)

    output_directory = save_dir + ion_implant + 'in' + cible + '\\' + nrj_km + 'eV'

    mainoutput_directory = save_dir + ion_implant + 'in' + cible

    os.makedirs(output_directory, exist_ok = True)

    TRIM.copy_output_files(srim_dir, output_directory)

    return mainoutput_directory
