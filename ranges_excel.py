# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:47:05 2023

@author: rnv
test file for range_excel function
"""

import time
import ray
import pandas as pd
import numpy as np
from scipy.stats import skewnorm
from scipy.stats import norm, kurtosis,skew, tmean,tvar

from srim import Layer, Target
from ranges import ranges_width
from wait_for_task import wait_for_tasks
from auto_srim import auto_srim

path=r"C:\Users\Documents\SRIMsim\"
ranges1,width1 = ranges_width(path)





import numpy as np

from scipy.stats import skewnorm

import matplotlib.pyplot as plt

kurt2=kurtosis(test[0:57,1]/np.sum(test[0:57,1]))
skewness2=skewnorm.skew(test[0:57,1])
mean=skewnorm.mean(test[0:57,1])
var=tvar(test[0:57,1])
pdffunc = extras.pdf_mvsk([1323, 904.7, -0.2128, 2.6706])
rangeh = np.arange(0, 5700, 0.1)
plt.plot(rangeh, pdffunc(rangeh))
plt.show()

fig, ax = plt.subplots(1, 1)
ax.hist(test[0:57,1],bins=58)

rng = np.random.default_rng(19680801)
N_points = 100000
n_bins = 20

# Generate two normal distributions
dist1 = rng.standard_normal(N_points)