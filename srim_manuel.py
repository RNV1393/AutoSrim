# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 14:17:30 2023

@author: rnv
"""

import os
import ray
import time
from srim import TRIM, Ion, Layer, Target


from math import log, floor

ray.shutdown()
time.sleep(5)
ray.init()

def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

# Construct a 3MeV Nickel ion

IonImplant='Mg'
Cible='AlN50nmGaN'

@ray.remote
def Srimauto(IonImplant,nrj):
    ion = Ion(IonImplant, energy=nrj)

    # Construct a layer of nick 20um thick with a displacement energy of 30 eV
    layer = Layer({
            'N': {
                'stoich': 1.0,
                'E_d': 28.0,
                'lattice': 3.0,
                'surface': 2.0
            },
            'Ga': {
                'stoich': 1.0,
                'E_d': 25.0,
                'lattice': 3.0,
                'surface': 2.82
            }}, density=6.15, width=5200)
    layer2 = Layer({
            'N': {
                'stoich': 1.0,
                'E_d': 28.0,
                'lattice': 3.0,
                'surface': 2.0
            },
            'Si': {
                'stoich': 1.0,
                'E_d': 15.0,
                'lattice': 2.0,
                'surface': 4.7
            }}, density=3.2, width=500)

    layer3= Layer({
                'N': {
                    'stoich': 1.0,
                    'E_d': 28.0,
                    'lattice': 3.0,
                    'surface': 2.0
                },
                'Al': {
                    'stoich': 1.0,
                    'E_d': 25.0,
                    'lattice': 3.0,
                    'surface': 3.36
                }}, density=3.255, width=500)


    # Construct a target of a single layer of Nickel
    target = Target([layer3,layer])

    # Initialize a TRIM calculation with given target and ion for 25 ions, quick calculation
    trim = TRIM(target, ion, number_ions=20000, calculation=1, angle_ions=9)

    # Specify the directory of SRIM.exe
    # For windows users the path will include C://...
    srim_executable_directory = r'C:\Softs\srim'

    # takes about 10 seconds on my laptop
    results = trim.run(r'C:\Softs\srim')
    # If all went successfull you should have seen a TRIM window popup and run 25 ions!
    a=human_format(nrj)
    output_directory = r'C:\Users\Documents\SRIMsim\100nm profile\\'+IonImplant+'in'+Cible+'\\'+a+'eV'
    os.makedirs(output_directory, exist_ok=True)
    TRIM.copy_output_files(r'C:\Softs\srim', output_directory)



nrjs=[30e3,35e3,40e3,45e3,50e3,55e3,60e3,65e3,70e3,75e3,80e3,85e3]
for nrj in nrjs:
    time.sleep(2)
    Srimauto.remote(nrj)
    time.sleep(2)
