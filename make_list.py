# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 17:02:44 2023

@author: rnv

ext must be strings
"""
import os

def make_list(path,ext) :
    """


    Parameters
    ----------
    path : string
        folder's path
    ext : string
        extensions to find

    Returns list of files and paths
    -------
    res : list
        list of path of ext files
    path : string
        DESCRIPTION.

    """

    # list to store txt files
    res = []
    # os.walk() returns subdirectories, file from current directory and
    # And follow next directory from subdirectory list recursively until last directory
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                res.append(os.path.join(root, file))

    #Tri par dates de modifications croissantes
    res = sorted(res, key=lambda t: os.stat(t).st_mtime)

    return res,path
