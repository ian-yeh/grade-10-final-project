#########################################
# File Name: main.py
# Description: the zombie apocalypse
# Author: Ian Yeh and Daniel
# Date: 05/24/2023
#########################################
import math
from random import randint
from pygame.locals import QUIT

import pygame, sys

# screen config/pygame set display
pygame.init()
WIDTH = 1200
HEIGHT = 720
TOP = 0
BOTTOM = 600
display = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255) 
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
grass = (98, 189, 98)
outline = 0

inPlay = True
scrollX = 0
scrollY = 0

scrollValue = randint(0,800)


# ---------------------------------------#
# classes                                #
# ---------------------------------------#
class gameObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class mapObject(gameObject):
    def __init__(self, x, y, width, height, colour, radius):
        super().__init__(x,y,width,height,)
        self.colour = colour
        self.radius = radius
        
"""class Guns(gameObject):
    def __init__(self, x, y, width, height, colour, name):
        super().__init__(x, y, width, height)
        self.colour = colour
        self.name = name

class Bullets(gameObject):
    def __init__(self, x, y, width, height, colour, name, xSpeed, ySpeed, damage):
        super().__init__(x, y, width, height)
        self.name = name
        self.colour = colour
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.damage = damage"""

class Entity:
    def __init__(self, x, y, width, height, hp, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.colour = colour

class Player(Entity):
    def __init__(self, x, y, width, height, hp, colour, killCount, money):
        super().__init__(x, y, width, height, hp, colour)
        self.killCount = killCount
        self.money = money

        # count bullets
        self.count = 0

    def show(self, screen):
        #pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        #pygame.draw.circle(screen, self.colour, (self.x, self.y), 30)
        #pygame.draw.circle(screen, self.colour, (self.x+20, self.y-20), 10)
        #pygame.draw.circle(screen, self.colour, (self.x-20, self.y-20), 10)
        #pygame.draw.circle(screen, self.colour, self.x+)
        self.spriteOrg = pygame.image.load("playerAnimation1.png")
        self.sprite = pygame.transform.scale(self.spriteOrg, (self.width, self.height))
        
        # get centrepoints of image
        #self.rect = self.sprite.get_rect()

        display.blit(self.sprite, (self.x, self.y))
        #display.blit(self.rect, (self.x, self.y))

    def playerRotate(self):
        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        self.angle = math.degrees(math.atan2(self.yDisplace, self.xDisplace))

        return self.angle

    def showGun(self, gunType):
        self.sprite = pygame.transform.rotate(self.spriteResize, self.playerRotate()/-2)
        pass

    def shoot(self, gunType, isShooting):
        self.isShooting = isShooting
        self.bulletX = self.x+self.width
        self.bulletY = self.y-(self.width/2)

        # draw bullet
        if isShooting:
            pygame.draw.rect(display, WHITE, (10, 10, 100, 100))

        print(self.count)
        
        if gunType == "pistol":
            self.damage = 5
        

class Zombie(Entity):
    def __init__(self, x, y, width, height, hp, colour, meleeDamage):
        super().__init__(x, y, width, height, hp, colour)
        self.meleeDamage = meleeDamage

    def show(self, screen): #draws zombie

        # moves zombie based on position compared to player
        if player.x-30 > self.x-scrollX: #player is to right
            self.x += zombieSpeed

        if player.x-30 < self.x-scrollX: # player is to left
            self.x -= zombieSpeed

        if player.y-30 > self.y-scrollY: # player is below zombie
            self.y += zombieSpeed

        if player.y-30 < self.y-scrollY: # player is above zombie
            self.y -= zombieSpeed

        pygame.draw.rect(screen, self.colour, (self.x-scrollX, self.y-scrollY, self.width, self.height))

        
# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    drawMap()
    drawPlayer()
    drawZombies()
    drawRocks()

    # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # shoots gun on left click
        if event.type == pygame.MOUSEBUTTONDOWN: #and event.button == 1: 

            player.shoot("pistol", True)
            player.count += 1

        #if event.type == pygame.MOUSEBUTTONUP:
         #   player.isShooting == False

    pygame.display.update()

def drawPlayer():
    player.show(display)

# random zombie x, y spawns
zombieX = []
zombieY = []
for i in range(700):
    zombieX.append(randint(0, 4000))
    zombieY.append(randint(0, 4000))

# create list of zombies
zombieList = []
for i in range(5):
    zombieList.append(Zombie(zombieX[i], zombieY[i], 50, 50, 100, GREEN, 5))

def drawZombies():
    for zombieNumber in range(len(zombieList)):
        zombieList[zombieNumber].show(display)

# create random coordinates for rock placement
rockX = []
rockY = []
rockSize = []
for i in range(1):
    rockX.append(randint(10, 3900))
    rockY.append(randint(10, 3900))
    rockSize.append(randint(200, 400))

rockImg = pygame.image.load("rock.png")
rockImg.set_colorkey(WHITE)

def drawRocks():
    for i in range(len(rockX)):
        #pygame.draw.rect(display, BLACK, (rockX[i]-scrollX, rockY[i]-scrollY, rockSize[i], rockSize[i]))
        newRock = pygame.transform.scale(rockImg, (rockSize[i], rockSize[i]))
        display.blit(newRock, (rockX[i]-scrollX, rockY[i]-scrollY))


def drawTrees():
    pass

def drawMap():
    # set colour for grass
    display.fill(grass)
    # set border
    pygame.draw.rect(display, BLACK, (0-scrollX, 0-scrollY, 4000,4000), 1)    
    # set border
    #pygame.draw.rect(display, BLACK, (scrollValue-scrollX, scrollValue-scrollY, 4000,4000), 1)  

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
player = Player(WIDTH/2-35, HEIGHT/2-35, 70, 70, 100, playerColour, 0, 0)
#player = Player(0, 0, 71, 71, 100, playerColour, 0, 0)
playerSpeed = 0.4
zombieSpeed = 0.1

# ---------------------------------------#
# main program                           #
# ---------------------------------------#
while inPlay:
    #print(player.x, player.y)
    #print(scrollX, scrollY)

    redrawGameWindow()

    #------move player-----#
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        inPlay = False
  
    #-----------check if player is in border----------#
    if (keys[pygame.K_a] and scrollX <= -548):
        scrollX = int(scrollX)

    elif keys[pygame.K_a]:
        scrollX -= playerSpeed
            
    if keys[pygame.K_d] and scrollX >= 3390:
        scrollX = int(scrollX)

    elif keys[pygame.K_d]:
        scrollX += playerSpeed

    if keys[pygame.K_w] and scrollY <= -308:
        scrollY = int(scrollY)

    elif keys[pygame.K_w]:
        scrollY -= playerSpeed
        
    if keys[pygame.K_s] and scrollY >= 3629:
        scrollY = int(scrollY)

    elif keys[pygame.K_s]:
        scrollY += playerSpeed

    #------------------------------------------------#
    
    pygame.event.clear()
    
    #-----------------------#

#---------------------------------------#
pygame.quit()
