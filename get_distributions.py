#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 20:26:24 2021

@author: karl
"""

import numpy as np
import pymssql
import pandas as pd

kit_pieces = ['snare','hi-hat-open','crash','ride','tom1','tom2','tom3','kick','hi-hat-pedal','hi-hat-closed']

kit_dict = np.load('kit_dict.npy',allow_pickle=True).item()

kit_dict['40'] = 'unknown'

server='localhost'
user='sa'
password='Munec@123'

conn = pymssql.connect(server,user,password,'midi_drum')

cursor = conn.cursor()

cursor.execute('SELECT * FROM Inputs')

data = cursor.fetchall()

data = [(kit_dict[str(entry[0])],entry[1]) for entry in data]

df = pd.DataFrame(data)

#%%
import matplotlib.pyplot as plt



for idx,piece in enumerate(kit_pieces):
    
    plt.figure(idx)
    plt.clf()
    ax = plt.gca()
    plt.title(piece)
    ax.title.set_fontsize(16)
    plt.xlabel('error (ms)')
    try:
        plt.hist(df[1][df[0]==piece])
        for item in [ax.xaxis.label]+ax.get_xticklabels():
            item.set_fontsize(16)

    except:
        pass