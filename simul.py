# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:13:15 2023

@author: rnv
"""

import time
import ray
import pandas as pd
import numpy as np

from srim import Layer, Target
from ranges import ranges_width
from wait_for_task import wait_for_tasks
from auto_srim import auto_srim



#### Inits pour faire tourner la fonction

#init de ray
ray.init(ignore_reinit_error = True)

#Dossier de l'exe de SRIM
srim_dir = r'C:\Softs\srim'

#Dossier de sauvegarde ne pas oublier \\ à la fin
save_dir = r'C:\Users\Documents\Test\\'

#définition de la structure
GaN = Layer({
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
        }}, density = 6.15, width = 10000, name='GaN')

SiN = Layer({
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
        }}, density = 3.17, width = 500, name = 'SiN') #width en Angstrom

target = Target([SiN,GaN]) # pour un empilement définir une autre layer et la positionner avant
#si c'est au dessus ou après si c'est en dessous

#Quel ion implanter
ion_implant = 'N'

#nom pour le dossier de sauvegarde
nomcibles = 'SiN50nmGaN'

#Nombre d'ion à simuler. A partir de 250k ça ne bouge plus trop
nb_ions = 1000

#Méthode de calcul"
"""
        (1) Ion Distribution and Quick Calculation of Damage (quick KP)
        (2) Detailed Calculation with full Damage Cascades (full cascades)
        (3) Monolayer Collision Steps / Surface Sputtering
        (4) Ions with specific energy/angle/depth (quick KP damage) using TRIM.DAT
        (5) Ions with specific energy/angle/depth (full cascades) using TRIM.DAT
        (6) Recoil cascades from neutrons, etc. (full cascades) using TRIM.DAT
        (7) Recoil cascades and monolayer steps (full cascades) using TRIM.DAT
        (8) Recoil cascades from neutrons, etc. (quick KP damage) using TRIM.DAT
"""
calc_method = 1

#Angle de l'ion
tilt = 9

#Taille intiale du matériau pour le premier tour
ini_width = 10000000

#matrice d'énergies
nrjs = [1e3,3e3, 5e3, 10e3, 15e3, 20e3, 30e3, 50e3, 75e3, 100e3, 125e3,
      150e3, 200e3, 300e3, 400e3, 500e3, 600e3, 700e3, 800e3, 900e3,
      1e6, 1.2e6, 1.35e6, 1.5e6]
nrjs = [1e3, 5e3, 10e3, 50e3, 100e3, 500e3] #pour aller vite/tests

#variables pour la boucle principale
i = 0
tour = 0
fixed_width = False
Width = 10000
##### Boucle principale pour les simulations

#Premier tour sur toutes les énergies avec une  épaisseur débilement grande et peu d'ions
if fixed_width == True:
    tour = 2

if tour == 0:
    GaN.width = ini_width
    for nrj in nrjs:
        pathID = auto_srim.remote(ion_implant,
            nomcibles+str(tour),500,tilt,nrj,target,calc_method,srim_dir,save_dir)
        time.sleep(1)
    wait_for_tasks() #attend que tous les processus lancés par ray soient finis
    simpath = ray.get(pathID)
    tour += 1

#Deuxième tour avec des épaisseurs plus adaptées et un plus grand
#nombre d'ions pour affiner l'épaisseur
if tour == 1:
    ranges1,width1 = ranges_width(simpath)
    data = pd.read_excel(width1,engine='openpyxl',header=None)
    data_ar = np.array(data)
    widths1 = data_ar[1:,3]
    nrjs1 = data_ar[1:,0]
    for nrj in nrjs1:
        GaN.width = widths1[i]
        time.sleep(1)
        pathID2 = auto_srim.remote(ion_implant,
            nomcibles+str(tour),2000,tilt,nrj,target,calc_method,srim_dir,save_dir)
        time.sleep(1)
        i += 1
    wait_for_tasks()
    simpath2 = ray.get(pathID2)
    tour += 1
    i = 0

#Troisième tour avec le nombre d'ions voulu
if tour == 2 and fixed_width == False:
    ranges2,width2=ranges_width(simpath2)
    data2 = pd.read_excel(width2,engine='openpyxl',header=None)
    data_ar2 = np.array(data2)
    widths2 = data_ar2[1:,3]
    nrjs2 = data_ar2[1:,0]
else:
    widths2=[Width for gg in range(len(nrjs))]
    nrjs2=nrjs
    for nrj in nrjs2:
        GaN.width = widths2[i]
        time.sleep(1)
        pathID3 = auto_srim.remote(ion_implant,
            nomcibles+str(tour),nb_ions,tilt,nrj,target,calc_method,srim_dir,save_dir)
        time.sleep(1)
        i += 1
    wait_for_tasks()
    simpath3 = ray.get(pathID3)
    ranges3,width3 = ranges_width(simpath3)

ray.shutdown() #on stoppe ray à la fin
