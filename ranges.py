# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:05:37 2023

@author: rnv
"""

import os
import re
import pandas as pd
from make_list import make_list
from range_excel import range_excel

def ranges_width(path):
    """


    Parameters
    ----------
    path : string
        path of RANGE.TXT

    Returns
    -------
    fname : string
        path of file ranges.xlsx
    fname2 : string
        path of file width.xlsx

    """
    res,path = make_list(path,".txt")
    res.sort(key=lambda f: float(re.sub(r'\D.\D','', os.path.split(os.path.split(f)[0])[1]))*float(
    re.search('[kKmM]',os.path.split(os.path.split(f)[0])[1])
    .group().replace('k', '1e3').replace('M', '1e6')))

    dfs = [] #pour mettre les donnés
    dfs2 =[]

    for line in res:
        head,tail=os.path.split(line)
        if tail != "RANGE.txt":
            pass
        else:
            df_out,df_out2=range_excel(line)
            head2,tail2=os.path.split(head)
            df_out.reset_index(inplace=True, drop=True)
            dfs.append(df_out)
            df_out2.reset_index(inplace=True, drop=True)
            dfs2.append(df_out2)

    final_data = pd.concat(dfs,axis=1)
    final_data2 =  pd.concat(dfs2)
    final_data2["Energy (eV)"]= (final_data2["Energy (eV)"].replace(r'[kKMeV]+$', '', regex=True)
                .astype(float) * \
                final_data2["Energy (eV)"].str.extract(r'[\d\.]+([kKM]+)', expand=False).fillna(1)
                .replace(['k','K','M'], [10**3,10**3, 10**6]).astype(int))
    fname = head2+"/Ranges.xlsx"
    final_data.to_excel(fname,header=False,index=False)
    fname2= head2+"/width.xlsx"
    final_data2.to_excel(fname2,header=True,index=False)
    return fname, fname2
