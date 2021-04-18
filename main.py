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
(width, height) = (700, 500)

rect = pygame.Rect(100,100,200,200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 1')
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
while True:
    timeNow = time.time()
    pygame.display.flip()
    screen.fill(background_colour)
    
    msg = inport.receive()
    
    if msg.type == 'note_on' and msg.velocity!=0 and msg.note!=21:
        print(msg)
        logThis.append(msg)
        
        this_note = msg.dict()['note']
        
        
        
        this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(500,(this_note-21)/30*400+50,5,10)}
    
        msglog.append(this_msg)
        pygame.draw.rect(screen,(0,0,0),msglog[-1]['rect'])
        
        
        
    if len(msglog)>0:
        try:
            while msglog[0]["due"]+10<time.time():
                msglog.popleft()
        except:
            print('caught exception during queue popping')
            
    for thisMsg in msglog:
        thisMsg['rect'].move_ip(-(time.time()-timeNow)/10*500,0)
        pygame.draw.rect(screen,(0,0,0),thisMsg['rect'])

#%%

mid = mido.MidiFile('Jazz5.mid')



for msg in mid.play():
    
    timeNow = time.time()
    pygame.display.flip()
    screen.fill(background_colour)
    
    outport.send(msg)
    
    
    print(msg)
    logThis.append(msg)
    
    this_note = msg.dict()['note']
    
    
    
    this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(500,(this_note-21)/30*400+50,5,10)}

    msglog.append(this_msg)
    pygame.draw.rect(screen,(0,0,0),msglog[-1]['rect'])
        
        
        
    if len(msglog)>0:
        try:
            while msglog[0]["due"]+10<time.time():
                msglog.popleft()
        except:
            print('caught exception during queue popping')
            
    for thisMsg in msglog:
        thisMsg['rect'].move_ip(-(time.time()-timeNow)/10*500,0)
        pygame.draw.rect(screen,(0,0,0),thisMsg['rect'])