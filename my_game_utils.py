#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 16:02:09 2021

@author: karl
"""

# bb format is (xMin,xMax,yMin,yMax)

def mouseInBB(mouse,bb):
    
    xMin,xMax,yMin,yMax = bb
    
    return mouse[0]>xMin and mouse[0]<xMax and mouse[1]>yMin and mouse[1]<yMax
    
    

def toggleChannels(channel_enabled,mouse,button_bb):
    
    
    toggleThis = [idx for idx,val in enumerate(button_bb) if mouseInBB(mouse,val)]
    
    if toggleThis:
        
        if channel_enabled[toggleThis[0]]:
            channel_enabled[toggleThis[0]] = False
        else:
            channel_enabled[toggleThis[0]] = True
    
    return channel_enabled
    