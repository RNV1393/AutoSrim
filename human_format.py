# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:30:06 2023

@author: rnv
"""
from math import log, floor

def human_format(number):
    """


    Parameters
    ----------
    number : float
        Transforms float into string with k M G etc...

    Returns string
    -------
    TYPE
        DESCRIPTION.

    """
    units = ['', 'k', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])
