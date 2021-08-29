#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 19:58:24 2021

@author: karl
"""

import mido
import time

print(mido.get_output_names()) # To list the output ports
print(mido.get_input_names()) # To list the input ports

inputs = mido.get_input_names()
outputs = mido.get_output_names()

inport = mido.open_input(inputs[0])
outport = mido.open_output(outputs[0])

kit_pieces = ['snare','hi-hat-open','crash','ride','tom1','tom2','tom3','kick','hi-hat-pedal','hi-hat-closed']
note_int = [None]

for piece in kit_pieces:
    
    hasNum = False
    
    print('waiting for: '+piece)
    
    while not hasNum:
        
        input_msg = inport.poll()
        
        if input_msg:
            if input_msg.type == 'note_on' and input_msg.dict()['note']!=note_int[-1]:
                this_note = input_msg.dict()['note']
                note_int.append(this_note)
                hasNum = True
                print(note_int)
                time.sleep(1)

        
        
note_int = note_int[1:]

kit_dict = {}

for piece,note_int in zip(kit_pieces,note_int):
    
    kit_dict[str(note_int)] = piece
    
import numpy as np

np.save('kit_dict.npy',kit_dict)
    