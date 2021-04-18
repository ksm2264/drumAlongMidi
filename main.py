#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 17:40:16 2019

@author: karl
"""
import mido
import time
from collections import deque
import matplotlib.pyplot as plt

#%%
import pygame

background_colour = (255,255,255)
(width, height) = (700, 1000)

rect = pygame.Rect(100,100,200,200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game')
screen.fill(background_colour)
# pygame.draw.rect(screen,(0,0,0),rect)
pygame.display.flip()
running = True




#%%
print(mido.get_output_names()) # To list the output ports
print(mido.get_input_names()) # To list the input ports

inputs = mido.get_input_names()
outputs = mido.get_output_names()

inport = mido.open_input(inputs[0])
outport = mido.open_output(outputs[0])

msglog = deque()
echo_delay = 2
logThis = list()
# msglog.append({"msg":inport.receive(),"due":time.time()+100})



#%%

import copy

mid = mido.MidiFile('Jazz5.mid')

all_msg = []

for msg in mid:
    if not msg.is_meta:
        all_msg.append(msg)

num_repeats = 3

for ii in range(num_repeats):
    
    all_msg += copy.deepcopy(all_msg)

unique_notes = [msg.note for msg in all_msg]

import numpy as np

unique_notes = list(np.unique(unique_notes))
unique_notes+=[40,48,49,45,43,44]
lastStart = time.time()


all_msg = deque(all_msg)

time_on_screen = 3

draw_input_time =0.2

msglog_input = deque()

play_soon_time = None

draw_delay = 1

sound_sender = deque()

y_pos = (time_on_screen-draw_delay)/time_on_screen*800

precision_level_seconds = 0.05

while len(all_msg)>0:
    
    timeNow = time.time()
    pygame.display.flip()
    screen.fill(background_colour)
    
    for notes in unique_notes:
        pygame.draw.circle(screen,(255,0,0),(unique_notes.index(notes)/len(unique_notes)*600+50,y_pos),25,2)

    
    if len(sound_sender)>0:
        sound = sound_sender[0]
        if timeNow-sound[1]>=draw_delay:
            outport.send(sound[0])
            sound_sender.popleft()
            
    if timeNow-lastStart>=all_msg[0].time:
        
        msg = all_msg[0]
        all_msg.popleft()
        
        msg.time=0
        
#        outport.send(msg)
        
        if msg.velocity!=0:
            
            print(msg)
            logThis.append(msg)
            
            this_note = msg.dict()['note']
            
            this_pos = unique_notes.index(this_note)
            
#            this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(this_pos/len(unique_notes)*600+50,800,50,20)} 
            this_msg = {"msg": msg, "due": time.time(), "circ": {'horiz':this_pos/len(unique_notes)*600+50}, "hit":False} 
            msglog.append(this_msg)
            
            sound_sender.append([msg,time.time()])
            
        lastStart = time.time()
            
            
    if len(msglog)>0:
        try:
            while msglog[0]["due"]+time_on_screen<time.time():
                msglog.popleft()
        except:
            print('caught exception during queue popping')
            
    for thisMsg in msglog:
        #thisRect = thisMsg['rect']
        
        scaleFac = (1-(timeNow-thisMsg['due'])/time_on_screen)
        
        newPosY = scaleFac*800
        #thisMsg['rect'].update(thisRect.left,newPosY,50*scaleFac,20*scaleFac)
        
        if not thisMsg['hit']:
            drawColor = (0,0,0)
        else:
            drawColor = (0,255,0)

        pygame.draw.circle(screen,drawColor,(thisMsg['circ']['horiz'],newPosY),22)

##        
    input_msg = inport.poll()
##    
    if input_msg:
        if input_msg.type == 'note_on':
            if input_msg.velocity!=0 and input_msg.note!=21:
            
                this_note = input_msg.dict()['note']
        #        
                this_pos = unique_notes.index(this_note)
        #        
                
        
#                this_msg = {"msg": input_msg, "due": time.time(), "rect": pygame.Rect(this_pos/len(unique_notes)*600+50,y_pos-5,50,10)} 
                this_msg = {"msg": input_msg, "due": time.time(), "circ": {'horiz':this_pos/len(unique_notes)*600+50}} 

                msglog_input.append(this_msg)
            
                
            
            
    if len(msglog_input)>0:
        for thisMsg in msglog_input:
            
            pygame.draw.circle(screen,(255,0,0),(thisMsg['circ']['horiz'],y_pos),25)
    #        
            this_note = thisMsg['msg'].note
            
            targ_info = [[idx,msg['due']+draw_delay-thisMsg['due']] for idx,msg in enumerate(msglog) if msg['msg'].note==this_note]
            
            mod_this = [val[0] for val in targ_info if abs(val[1]<precision_level_seconds)]
            
            if mod_this:
                msglog[mod_this[0]]['hit']=True
        
    try:
        while msglog_input[0]["due"]+draw_input_time<time.time():
            msglog_input.popleft()
    except:
        print('caught exception during queue popping')
            
        
        