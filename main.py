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
import rtmidi

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
#while True:
#    timeNow = time.time()
#    pygame.display.flip()
#    screen.fill(background_colour)
#    
#    msg = inport.receive()
#    
#    if msg.type == 'note_on' and msg.velocity!=0 and msg.note!=21:
#        print(msg)
#        logThis.append(msg)
#        
#        this_note = msg.dict()['note']
#        
#        
#        
#        this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(500,(this_note-21)/30*400+50,5,10)}
#    
#        msglog.append(this_msg)
#        pygame.draw.rect(screen,(0,0,0),msglog[-1]['rect'])
#        
#        
#        
#    if len(msglog)>0:
#        try:
#            while msglog[0]["due"]+10<time.time():
#                msglog.popleft()
#        except:
#            print('caught exception during queue popping')
#            
#    for thisMsg in msglog:
#        thisMsg['rect'].move_ip(-(time.time()-timeNow)/10*500,0)
#        pygame.draw.rect(screen,(0,0,0),thisMsg['rect'])

#%%


mid = mido.MidiFile('Jazz5.mid')

all_msg = []

for msg in mid:
    if not msg.is_meta:
        all_msg.append(msg)

unique_notes = [msg.note for msg in all_msg]

import numpy as np

unique_notes = list(np.unique(unique_notes))
unique_notes+=[40,48,49,45,43,44]
lastStart = time.time()


all_msg = deque(all_msg)

time_on_screen = 5

msglog_input = deque()

while len(all_msg)>0:
    
    timeNow = time.time()
    pygame.display.flip()
    screen.fill(background_colour)
    
    
    if timeNow-lastStart>=all_msg[0].time:
        
        msg = all_msg[0]
        all_msg.popleft()
        
        msg.time=0
        
        outport.send(msg)
        
        if msg.velocity!=0:
            
            print(msg)
            logThis.append(msg)
            
            this_note = msg.dict()['note']
            
            this_pos = unique_notes.index(this_note)
            
            this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(this_pos/len(unique_notes)*600+50,800,50,20)} 
            msglog.append(this_msg)
            pygame.draw.rect(screen,(0,0,0),msglog[-1]['rect'])
            
        lastStart = time.time()
            
            
    if len(msglog)>0:
        try:
            while msglog[0]["due"]+time_on_screen<time.time():
                msglog.popleft()
        except:
            print('caught exception during queue popping')
            
    for thisMsg in msglog:
        thisRect = thisMsg['rect']
        
        scaleFac = (1-(timeNow-thisMsg['due'])/time_on_screen)
        
        newPosY = scaleFac*800
        thisMsg['rect'].update(thisRect.left,newPosY,50*scaleFac,20*scaleFac)
        pygame.draw.rect(screen,(0,0,0),thisMsg['rect'])
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
                this_msg = {"msg": input_msg, "due": time.time(), "rect": pygame.Rect(this_pos/len(unique_notes)*600+50,800,50,10)} 
            
                msglog_input.append(this_msg)
                pygame.draw.rect(screen,(255,0,0),msglog_input[-1]['rect'])
            
            
            
    if len(msglog_input)>0:
        try:
            while msglog_input[0]["due"]+10<time.time():
                msglog_input.popleft()
        except:
            print('caught exception during queue popping')
            
    for thisMsg in msglog_input:
        thisRect = thisMsg['rect']
        
        scaleFac = (1-(timeNow-thisMsg['due'])/time_on_screen)
        
        newPosY = scaleFac*800
        thisMsg['rect'].update(thisRect.left,newPosY,50*scaleFac,10*scaleFac)
        pygame.draw.rect(screen,(255,0,0),thisMsg['rect'])
#        