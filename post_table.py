#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 22:37:32 2021

@author: karl
"""

import pymssql
import numpy as np

table_list = list(np.load('table_out_test.npy'))

server='localhost'
user='sa'
password='Munec@123'

conn = pymssql.connect(server,user,password,'midi_drum')

cursor = conn.cursor()

for entry in table_list:
    
    second_str = entry[1]
    if second_str=='missed':
        second_str='null'
    
    cursor.execute("INSERT INTO Inputs (note,time) VALUES ({this_note}, {this_time})".format(this_note=entry[0],this_time=second_str))

cursor.execute('SELECT * FROM Inputs')
conn.commit()

for row in cursor:
    print('row = %r' % (row,))

conn.close()