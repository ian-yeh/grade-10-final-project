#########################################
# File Name: main.py
# Description: the zombie apocalypse
# Author: Ian Yeh and Daniel
# Date: 05/24/2023
#########################################
import math
from random import randint, choice
from pygame.locals import QUIT

import pygame, sys

# screen config/pygame set display
pygame.init()
clock = pygame.time.Clock()
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

class Gun():
    def __init__(self, x, y, picture):
        self.x = x
        self.y = y
 
        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        self.angle = math.radians(math.degrees(math.atan2(self.yDisplace, self.xDisplace)))

        self.load = pygame.image.load(picture)
        self.image = pygame.transform.scale(self.load,(40, 40))
        

    def show(self):
        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        self.angle = math.radians(math.degrees(math.atan2(self.yDisplace, self.xDisplace)))

        self.sprite = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        display.blit(self.sprite, (self.x, self.y))

class Crosshair():
    def __init__(self):
        self.image = pygame.image.load("crosshair.png")

    def show(self):
        self.mouseCoords = pygame.mouse.get_pos()
        display.blit(self.image, (self.mouseCoords[0]-20, self.mouseCoords[1]-20))

        

class Bullets():
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage  

        self.angle = math.radians(math.degrees(math.atan2(guns[0].yDisplace, guns[0].xDisplace)))
        
        self.xSpeed = 14 * math.cos(self.angle)
        self.ySpeed = 14 * math.sin(self.angle)

        # load bullet png, rotate to angle of shot
        self.image = pygame.image.load("bullet.png")
        self.bullet = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = self.bullet.get_rect()

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.killCount = 0
        self.money = 0

        self.hp = 400

        self.level = 0
        self.levelProgress = 0

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

        self.reachCheck = False
        self.checkPointX = choice(range(200, 1000, 2))
        self.checkPointY = choice(range(100, 600, 2))

    def show(self): #draws zombie
        if self.reachCheck == False:
            # moves zombie based on position compared to player
            if self.checkPointX > self.x-scrollX: #player is to right
                self.x += zombieSpeed

            if self.checkPointX < self.x-scrollX: # player is to left
                self.x -= zombieSpeed

            if self.checkPointY > self.y-scrollY: # player is below zombie
                self.y += zombieSpeed

            if self.checkPointY < self.y-scrollY: # player is above zombie
                self.y -= zombieSpeed

            if -5 <= (self.x-self.checkPointX) <= 5 and -5 <= (self.y-self.checkPointY) <= 5:
                self.reachCheck = True

        elif self.reachCheck == True:
            # moves zombie based on position compared to player
            if player.x-30 > self.x-scrollX: #player is to right
                self.x += zombieSpeed

            if player.x-30 < self.x-scrollX: # player is to left
                self.x -= zombieSpeed

            if player.y-30 > self.y-scrollY: # player is below zombie
                self.y += zombieSpeed

            if player.y-30 < self.y-scrollY: # player is above zombie
                self.y -= zombieSpeed

        #print(self.reachCheck, (self.x, self.y), (self.checkPointX, self.checkPointY))

        #pygame.draw.rect(display, RED, (self.x-scrollX+30, self.y-scrollY+10, 70, 70), 1)
        display.blit(self.sprite, (self.x-scrollX, self.y-scrollY))

        
# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    pygame.mouse.set_visible(False)

    drawMap()
    drawPlayer()
    drawZombies()
    drawRocks()
    drawGun()

    healthBar()
    levelBar()

    drawBullets()
    updateBullets()
    checkCollisions()

    drawCrosshair()

    clock.tick(60)
    pygame.display.update()

def drawPlayer():
    player.show(display)

def drawCrosshair():
    crosshair.show()

def drawZombies():
    # draw zombie
    for zombieNumber in range(len(zombieList)):
        zombieList[zombieNumber].show()

    # draw zombie health bar
    for z in zombieList:
        pygame.draw.rect(display, RED, (z.x-scrollX+32, z.y+2-scrollY, 60, 6))
        pygame.draw.rect(display, GREEN, (z.x-scrollX+32, z.y+2-scrollY, (z.hp/zombieLevelHP[player.level])*60, 6))

        if z.hp <= 0:
            zombieList.remove(z)
            player.killCount+=1
            player.levelProgress+=1  

def drawRocks():
    for i in range(len(rockX)):
        newRock = pygame.transform.scale(rockImg, (rockSize[i], rockSize[i]))
        display.blit(newRock, (rockX[i]-scrollX, rockY[i]-scrollY))

def drawTrees():
    pass

def drawMap():
    # set colour for grass
    display.fill(BLACK)
    # set border
    pygame.draw.rect(display, grass, (0-scrollX, 0-scrollY, 4000,4000))    
    # set border
    #pygame.draw.rect(display, BLACK, (scrollValue-scrollX, scrollValue-scrollY, 4000,4000), 1)  

def drawGun():
    guns[0].show()

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
        if len(bullets) == 0:
            print("hasdfasdgi")
            break 
        for z in zombieList:
            
            if (b.x>=z.x-scrollX+30 and b.x<=(z.x+70-scrollX)) and (b.y>=z.y-scrollY+10 and b.y<=(z.y+70-scrollY)):
            
                print('hit')
                z.hp -= 5

                if len(bullets) <= 1:
                    print(",,,,,,,,,,,,,,,,,,,,")
                    break
                    
                print("YEOA:FKLJ:LAKDFJ")
                bullets.remove(b)
                        

def healthBar():
    pygame.draw.rect(display, RED, (40,600,400,30))
    pygame.draw.rect(display, neonGreen, (40,600,player.hp,30))

def levelBar():
    levelProgress = (player.levelProgress/zombieLevelSpawn[player.level])*400
    if levelProgress > 400:
        levelProgress = 400
    pygame.draw.rect(display, WHITE, (40,645,400,20))
    pygame.draw.rect(display, BLACK, (40,645,levelProgress,20))

    if player.levelProgress == zombieLevelSpawn[player.level]:
        player.levelProgress = 0
        player.level += 1

def drawStats():
    pass

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
player = Player((WIDTH/2)-35, (HEIGHT/2)-35)
#player = Player(0, 0, 71, 71, 100, playerColour, 0, 0)
playerSpeed = 5
zombieSpeed = 1.5

zombieLevelHP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
zombieLevelSpawn = [100, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]

crosshair = Crosshair()

# create random coordinates for rock placement
rockX = []
rockY = []
rockSize = []
for i in range(100):
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

# list of guns
waterGun = Gun(player.x+20, player.y+20, "water gun.png")

guns = [waterGun]

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
        if event.type == pygame.MOUSEBUTTONDOWN: 
            bullets.append(Bullets(player.x+30, player.y+30, 1))

            player.hp -= 1

    #------move player-----#
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        inPlay = False
  
    #-----------check if player is in border----------#
    if (keys[pygame.K_a] and scrollX <= -563):
        scrollX = int(scrollX)

    elif keys[pygame.K_a]:
        scrollX -= playerSpeed
            
    if keys[pygame.K_d] and scrollX >= 3365:
        scrollX = int(scrollX)

    elif keys[pygame.K_d]:
        scrollX += playerSpeed

    if keys[pygame.K_w] and scrollY <= -325:
        scrollY = int(scrollY)

    elif keys[pygame.K_w]:
        scrollY -= playerSpeed
        
    if keys[pygame.K_s] and scrollY >= 3610:
        scrollY = int(scrollY)

    elif keys[pygame.K_s]:
        scrollY += playerSpeed

    #------------------------------------------------#
    
    redrawGameWindow()

    #-----------------------#

#---------------------------------------#
pygame.quit()
