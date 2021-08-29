#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 20:50:12 2021

@author: karl
"""

import pygame
from menu_utils import createRect,launchGame
from my_game_utils import mouseInBB
import glob

songList = glob.glob('*.mid') + glob.glob('*.midi')


background_colour = (255,255,255)
(width, height) = (700, 1000)

rect = pygame.Rect(100,100,200,200)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game')
screen.fill(background_colour)
# pygame.draw.rect(screen,(0,0,0),rect)
pygame.display.flip()

running = True

rect_bb_list=[]


 # will need to handle overflow with prev/next buttons later
for idx,mid_str in enumerate(songList):
    
    this_bb=createRect(mid_str,idx,screen)

    rect_bb_list.append(this_bb)
    
while running:
    pygame.display.flip()

    
   
    
    for ev in pygame.event.get():
            
        if ev.type==pygame.QUIT:
            pygame.quit()
        
        
        if ev.type == pygame.MOUSEBUTTONDOWN:
            
            mouse = pygame.mouse.get_pos()
            print(mouse)
            
            for idx,bb in enumerate(rect_bb_list):
                
                if mouseInBB(mouse,bb):
                    
                    this_song_name = songList[idx]
                    running=False
                    pygame.quit()




#%% game
                    
import mido
import time
from collections import deque
import matplotlib.pyplot as plt

#%%
import pygame

from my_game_utils import toggleChannels

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

mid = mido.MidiFile(this_song_name)

write_msg_log = []

all_msg = []

for msg in mid:
    if not msg.is_meta:
        all_msg.append(msg)

num_repeats = 5

for ii in range(num_repeats):
    
    all_msg += copy.deepcopy(all_msg)

#all_msg = all_msg*5

unique_notes = [msg.note for msg in all_msg]

import numpy as np

unique_notes = list(np.unique(unique_notes))
unique_notes+=[23,46,40,48,49,45,43,44]
unique_notes = list(np.unique(unique_notes))
lastStart = time.time()


all_msg = deque(all_msg)

time_on_screen = 3

draw_input_time =0.2

msglog_input = deque()

play_soon_time = None

draw_delay = 1

sound_sender = deque()

y_pos = (time_on_screen-draw_delay)/time_on_screen*800

precision_level_seconds_perfect = 0.025
precision_level_seconds_acceptable = 0.05

channel_enabled = [True]*len(unique_notes)

button_bb = []

for notes in unique_notes:
    
    
    x_cen = unique_notes.index(notes)/len(unique_notes)*600+50
    y_cen = 950
    
    button_bb.append((x_cen-25,x_cen+25,y_cen-25,y_cen+25))
    

while len(all_msg)>0:
    
    timeNow = time.time()
    pygame.display.flip()
    screen.fill(background_colour)
    
    for idx,notes in enumerate(unique_notes):
        pygame.draw.circle(screen,(255,0,0),(unique_notes.index(notes)/len(unique_notes)*600+50,y_pos),25,2)

        if channel_enabled[idx]:
            drawWidth = 0
        else:
            drawWidth = 2
            
        pygame.draw.circle(screen,(122,122,0),(unique_notes.index(notes)/len(unique_notes)*600+50,950),25,drawWidth)

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
            
            #print(msg)
            
            this_note = msg.dict()['note']
            
            this_pos = unique_notes.index(this_note)
            
#            this_msg = {"msg": msg, "due": time.time(), "rect": pygame.Rect(this_pos/len(unique_notes)*600+50,800,50,20)} 
            
            if channel_enabled[this_pos]:
                this_msg = {"msg": msg, "due": time.time(), "circ": {'horiz':this_pos/len(unique_notes)*600+50}, "hit":'no'} 
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
        
        if thisMsg['hit']=='no':
            drawColor = (0,0,0)
        elif thisMsg['hit']=='perfect':
            drawColor = (0,255,0)
        elif thisMsg['hit']=='slow':
            drawColor = (255,0,255)
        elif thisMsg['hit']=='fast':
            drawColor = (0,0,255)

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
                this_msg = {"msg": input_msg, "due": time.time(), "circ": {'horiz':this_pos/len(unique_notes)*600+50}, "status":"missed"} 

                msglog_input.append(this_msg)
            
                
            
            
    if len(msglog_input)>0:
        for thisMsg in msglog_input:
            
            pygame.draw.circle(screen,(255,0,0),(thisMsg['circ']['horiz'],y_pos),25)
    #        
            this_note = thisMsg['msg'].note
            
            targ_info = [[idx,msg['due']+draw_delay-thisMsg['due']] for idx,msg in enumerate(msglog) if msg['msg'].note==this_note]
            
            mod_this = [val for val in targ_info if abs(val[1])<precision_level_seconds_acceptable]
            
            if mod_this:
                
                thisMsg['status'] = mod_this[0][1]
                
                if abs(mod_this[0][1])<precision_level_seconds_perfect:
                    msglog[mod_this[0][0]]['hit']='perfect'
                elif mod_this[0][1]>0:
                    msglog[mod_this[0][0]]['hit']='slow'
                elif mod_this[0][1]<0:
                    msglog[mod_this[0][0]]['hit']='fast'                
    try:
        while msglog_input[0]["due"]+draw_input_time<time.time():
            write_msg_log.append(msglog_input[0])
            msglog_input.popleft()
    except:
        pass
            
    for ev in pygame.event.get():
        
        if ev.type==pygame.QUIT:
            pygame.quit()
            
        if ev.type == pygame.MOUSEBUTTONDOWN:
            
            mouse = pygame.mouse.get_pos()
            
            channel_enabled = toggleChannels(channel_enabled,mouse,button_bb)
            
        
table_out = []
        
            
for msg in write_msg_log:
    
    table_out.append([msg['msg'].note,msg['status']])
    
np.save('table_out_test.npy',table_out)
