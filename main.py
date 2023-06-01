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
RED = (250, 0, 0)
grass = (98, 189, 98)
neonGreen = (57, 255, 20)
outline = 0

inPlay = True
scrollX = 0
scrollY = 0


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

class Bullets():
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage  
        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        self.angle = math.radians(math.degrees(math.atan2(self.yDisplace, self.xDisplace)))
        
        self.xSpeed = 1.3 * math.cos(self.angle)
        self.ySpeed = 1.3 * math.sin(self.angle)

        # load bullet png, rotate to angle of shot
        self.image = pygame.image.load("bullet.png")
        #self.imageResize = pygame.transform.scale(self.image, (10, 10))
        self.bullet = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = self.bullet.get_rect()
       
class Entity:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.killCount = 0
        self.money = 0

        self.hp = 400

        self.level = 0

        # count bullets
        self.count = 0

    def show(self, screen):
        self.spriteOrg = pygame.image.load("playerAnimation1.png")
        self.sprite = pygame.transform.scale(self.spriteOrg, (70, 70))

        display.blit(self.sprite, (self.x, self.y))

    def playerRotate(self):
        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        self.angle = math.degrees(math.atan2(self.yDisplace, self.xDisplace))

        return self.angle

    def showGun(self, gunType):
        self.sprite = pygame.transform.rotate(self.spriteResize, self.playerRotate()/-2)
        pass
        

class Zombie():
    def __init__(self, x, y, hp, level):
        self.x = x
        self.y = y 

        self.hp = hp   

        self.level = level

        self.meleeDamage = 10

        self.image = pygame.image.load("zombie.png")
        self.sprite = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.sprite.get_rect()

    def show(self): #draws zombie

        # moves zombie based on position compared to player
        if player.x-30 > self.x-scrollX: #player is to right
            self.x += zombieSpeed

        if player.x-30 < self.x-scrollX: # player is to left
            self.x -= zombieSpeed

        if player.y-30 > self.y-scrollY: # player is below zombie
            self.y += zombieSpeed

        if player.y-30 < self.y-scrollY: # player is above zombie
            self.y -= zombieSpeed

        
        #pygame.draw.rect(screen, self.colour, (self.x-scrollX, self.y-scrollY, self.width, self.height))
        display.blit(self.sprite, (self.x-scrollX, self.y-scrollY))

        
# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    drawMap()
    drawPlayer()
    drawZombies()
    drawZombieHitbox()
    drawRocks()

    healthBar()
    levelBar()

    drawBullets()
    updateBullets()
    checkCollisions()

    pygame.time.delay(1)
    pygame.display.update()

def drawPlayer():
    player.show(display)

def drawZombies():
    for zombieNumber in range(len(zombieList)):
        zombieList[zombieNumber].show()

    for z in zombieList:
        pygame.draw.rect(display, RED, (z.x-scrollX+32, z.y+2-scrollY, 60, 6))
        pygame.draw.rect(display, GREEN, (z.x-scrollX+32, z.y+2-scrollY, (z.hp/zombieLevelHP[player.level])*60, 6))

        if z.hp <= 0:
            zombieList.remove(z)

def drawZombieHitbox():
    #for z in zombieList:
     #   pygame.draw.rect(display, RED, (z.x-scrollX+30, z.y-scrollY+10, 70, 70), 1)
    pass

def drawRocks():
    for i in range(len(rockX)):
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

def drawBullets():
    for b in bullets:
        #pygame.draw.rect(display, (0,0,0), (b.x,b.y,15,15)) 
        display.blit(b.bullet, (b.x, b.y))

def updateBullets():
    for b in bullets:
        b.y += b.ySpeed
        b.x += b.xSpeed

        if 0 >= b.x or 1200 <= b.x:
            bullets.remove(b)

        if 0 >= b.y or 700 <= b.y:
            bullets.remove(b)

def checkCollisions():
    for b in bullets:
        for z in zombieList:
            #pygame.draw.rect(display, RED, (z.x-scrollX+30, z.y-scrollY+10, 70, 70), 1)
            
            if (b.x>=z.x-scrollX+30 and b.x<=(z.x+70-scrollX)) and (b.y>=z.y-scrollY+10 and b.y<=(z.y+70-scrollY)):
            
                print('hit')
                z.hp -= 5

                if len(bullets) > 0:
                    bullets.remove(b)
  
def healthBar():
    pygame.draw.rect(display, RED, (40,600,400,30))
    pygame.draw.rect(display, neonGreen, (40,600,player.hp,30))

def levelBar():
    levelProgress = (player.killCount/zombieLevelSpawn[player.level])*400
    if levelProgress > 400:
        levelProgress = 400
    pygame.draw.rect(display, WHITE, (40,645,400,20))
    pygame.draw.rect(display, BLACK, (40,645,levelProgress,20))

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
player = Player((WIDTH/2)-35, (HEIGHT/2)-35)
#player = Player(0, 0, 71, 71, 100, playerColour, 0, 0)
playerSpeed = 0.6
zombieSpeed = 0.2

zombieLevelHP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
zombieLevelSpawn = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]

# create random coordinates for rock placement
rockX = []
rockY = []
rockSize = []
for i in range(20):
    rockX.append(randint(10, 3900))
    rockY.append(randint(10, 3900))
    rockSize.append(randint(50, 150))

rockImg = pygame.image.load("rock.png")
rockImg.set_colorkey(WHITE)

# random zombie x, y spawns
zombieX = []
zombieY = []
for i in range(200):
    zombieX.append(randint(1000, 4000))
    zombieY.append(randint(350, 4000))

# create list of zombies
zombieList = []
for i in range(zombieLevelSpawn[player.level]):
    zombieList.append(Zombie(zombieX[i], zombieY[i], 10, 1))

# list for bullets
bullets = []

# ---------------------------------------#
# main program                           #
# ---------------------------------------#
while inPlay:
    # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # shoots gun on left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 

            bullets.append(Bullets(player.x+30, player.y+30, 1))
            player.killCount += 1
            player.hp -= 10

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
    
    redrawGameWindow()

    #-----------------------#

#---------------------------------------#
pygame.quit()
