'''
Author: Ian Lim 
Date: 9/10/25
Purpose:
External Sources:
'''

from config import *
import pygame

class State:
    def __init__(self):
        self.mines = MINES
        self.flags = 0
        self.gameOver = False 
        self.victory = False
        
            
    def updateMine(self,font,screen):
        self.mines -= 1
        mineCounter = font.render(str(self.mines),True, blue)
        screen.bilt(mineCounter,(0,0))

    def updateFlag(self,font,screen):
        self.flags += 1
        remainingFlags = self.mines-self.flags
        flagCounter = font.render(str(remainingFlags),True, blue)
        screen.bilt(flagCounter,(360,0))
