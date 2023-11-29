# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 15:54:17 2023

@author: rnv

"""

import csv
import os
import re
import pandas as pd
import numpy as np

def range_excel(path):

    head,tail=os.path.split(path)
    head2,tail2=os.path.split(head)
    rows=[]
    with open(path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            row=line.replace(',','.')
            rows.append(row)

    with open('dummy.txt','w') as file:
        for row in rows:
            file.write(row)

    rows2=[]
    with open('dummy.txt', 'r') as file:
        reader = csv.reader(file, delimiter = '\t')
        for row2 in reader:
            rows2.append(row2)

    df = pd.DataFrame(rows2)
    a = df[0].str.find("DEPTH")
    a = a.fillna(-1)
    a = (a[a != -1].index).tolist()
    a = a[0]

    b = df[0].str.find("Total Ions calculated")
    b = b.fillna(-1)
    b = (b[b != -1].index).tolist()
    b = b[0]
    ionrange = df[b+1:b+4]

    c = df[0].str.find("Range Skewne")
    d = df[0].str.find("Range Kurtosis")
    c = c.fillna(-1)
    d = d.fillna(-1)
    c = (c[c != -1].index).tolist()[0]
    d = (d[d != -1].index).tolist()[0]

    skewness= df.iloc[c]
    kurtosis= df.iloc[d]

    df = df[a-1:]
    df = df.reset_index()
    df = df.drop(columns=df.columns[0], axis=1)
    df2 = df[0].apply(lambda x: pd.Series(str(x).split(' ')))
    df = df2.drop(columns=df2.columns[1], axis=1).drop(
        columns=df2.columns[3], axis=1).drop(columns=df2.columns[4], axis=1)
    header = ['Depth (Ang)', 'Ions', 'Concentration']
    df3 = df.drop(columns=df.columns[2:], axis=1)
    df3.drop([0, 1, 2, 3], axis=0, inplace=True)
    df3 = df3.reset_index()
    df3 = df3.drop(columns=df3.columns[0], axis=1)

    df3[""] = np.nan
    df3.columns = [0, 1, 2]
    df3 = df3.astype(float)
    headers = pd.DataFrame([header])

    df4 = pd.DataFrame([[tail2, '', '']])
    df5 = pd.concat([df4, headers, df3])

    ionrange.reset_index(inplace=True, drop=True)
    ionrange4=ionrange[0].loc[0]
    res=np.float_(re.findall(r"[-+]?(?:\d*\.*\d+)", ionrange4))
    width=res[0]*10**res[1]+5*res[2]*10**res[3] #Should be changed

    skewness.reset_index(inplace=True, drop=True)
    skewness2=skewness[0]
    skewness2=np.float_(re.findall(r"[-+]?(?:\d*\.*\d+)", skewness2))

    kurtosis.reset_index(inplace=True, drop=True)
    kurtosis2=kurtosis[0]
    kurtosis2=np.float_(re.findall(r"[-+]?(?:\d*\.*\d+)", kurtosis2))

    df6=pd.DataFrame([[tail2, res[0]*10**res[1], res[2]*10**res[3], width,
                       skewness2[0],kurtosis2[0]]],
                     columns=['Energy (eV)','Longitudinal Range (Ang)','Straggling (Ang) ' ,
                              'Width (Ang)', 'Skewness','Kurtosis'])
    os.remove("dummy.txt")
    return df5,df6
