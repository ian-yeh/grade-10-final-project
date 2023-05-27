import pygame, sys
from pygame.locals import QUIT
#########################################
# File Name: drawingText.py
# Description: This program demonstrates how to draw text in Pygame.
# Author: Daniel Hu
# Date: 27/03/2023
#########################################

pygame.init()
WIDTH = 800
HEIGHT= 600
display = pygame.display.set_mode((WIDTH,HEIGHT))

GREEN = (  0,255,  0)
WHITE = (255,255,255)
RED = (255, 0, 0)
font = pygame.font.SysFont("Courier New Bold",36)
inPlay = True

def drawBullet():
    pygame.draw.rect()

#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
while inPlay:
    pygame.event.clear()
    gameWindow.fill(WHITE)
    
    

       # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawBullet()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        inPlay = False
        
    pygame.display.update()             # display must be updated, in order
                                        # to show the drawings