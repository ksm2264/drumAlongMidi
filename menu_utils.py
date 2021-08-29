#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 20:58:03 2021

@author: karl
"""

import pygame

def createRect(song_name,song_num,screen):
    
    
    black = (0,0,0)
    white = (255,255,255)
    
    pygame.init()
    my_font = pygame.font.SysFont('Arial',25)
    
    this_bb = (100,100+song_num/14*800,200,50)
    
    pygame.draw.rect(screen,black,this_bb)
    screen.blit(my_font.render(song_name,True,white),(100,100+song_num/14*800))
    
    this_bb = (this_bb[0],this_bb[0]+this_bb[2],this_bb[1],this_bb[1]+this_bb[3])
    return this_bb
    
def launchGame():
    
    return None