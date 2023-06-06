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
HEIGHT = 700
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

font = pygame.font.Font('CaviarDreams.ttf', 15)
font2 = pygame.font.Font("CaviarDreams.ttf", 30)

inPlay = True
gameEnd = False
scrollX = 0
scrollY = 0

frameRateMultiplier = 2.2


# ---------------------------------------#
# ---------------------------------------#
class Crate:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def show(self):
        self.image = pygame.image.load("crate.png")
        self.sprite = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.sprite.get_rect()

        display.blit(self.sprite, (self.x-scrollX, self.y-scrollY))

class Gun:
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


        if self.mouseCoords[0] >= WIDTH/2:
            self.sprite = pygame.transform.rotate(self.image, -math.degrees(self.angle))

        else:
            self.sprite = pygame.transform.flip(pygame.transform.rotate(self.image, math.degrees(self.angle)), False, True)

        display.blit(self.sprite, (self.x, self.y))

class Crosshair:
    def __init__(self):
        self.image = pygame.image.load("crosshair.png")

    def show(self):
        self.mouseCoords = pygame.mouse.get_pos()
        display.blit(self.image, (self.mouseCoords[0]-20, self.mouseCoords[1]-20))

class Bullets:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage  

        self.angle = math.radians(math.degrees(math.atan2(guns[0].yDisplace, guns[0].xDisplace)))
        
        self.xSpeed = 14*frameRateMultiplier * math.cos(self.angle)
        self.ySpeed = 14*frameRateMultiplier * math.sin(self.angle)

        # load bullet png, rotate to angle of shot
        self.image = pygame.image.load("bullet.png")

        self.bullet = pygame.transform.rotate(self.image, -math.degrees(self.angle))
      
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        
class Player:
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
        self.mouseCoords = pygame.mouse.get_pos()
        self.spriteOrg = pygame.image.load("playerAnimation1.png")

        

        if self.mouseCoords[0] >= WIDTH/2:
            self.sprite = pygame.transform.scale(self.spriteOrg, (70, 70))
            

        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(self.spriteOrg, (70, 70)), True, False)

        self.rect = self.sprite.get_rect()
        
        display.blit(self.sprite, (self.x, self.y))

class Zombie:
    def __init__(self, x, y, hp, damage):
        self.x = x
        self.y = y 

        self.hp = hp   

        self.damage = damage

        self.image = pygame.image.load("zombie.png")
        self.sprite = pygame.transform.scale(self.image, (120, 120))
        #self.rect = self.sprite.get_rect()
        

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

            if -5 <= (self.x-self.checkPointX-scrollX) <= 5 and -5 <= (self.y-self.checkPointY-scrollY) <= 5:
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
        self.rect = pygame.Rect(self.x-scrollX+30, self.y-scrollY+10, 70,70)
        pygame.draw.rect(display, RED, self.rect, 1)
        display.blit(self.sprite, (self.x-scrollX, self.y-scrollY))
        

        
# ---------------------------------------#
# functions                             #
# ---------------------------------------#
def redrawGameWindow():
    pygame.mouse.set_visible(False)

    drawMap()
    drawPlayer()
    drawZombies()
    drawGun()

    healthBar()
    levelBar()

    drawBullets()
    checkCollisions()
    updateBullets()
    bulletTracker()

    zombieHit()

    drawCrosshair()
    drawCrates()

    if gameEnd == True:
        pygame.mouse.set_visible(True)
        endScreen()

    clock.tick(30)
    pygame.display.update()

def endScreen():
    display.fill((100, 150, 200))


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

def drawCrates():
    for crate in crates:
        crate.show()

        pygame.draw.rect(display, RED, (crate.x-scrollX, crate.y-scrollY, crate.size, crate.size), 1)

        if (player.x>=crate.x and player.x<=crate.x+crate.size) and (player.y>=crate.y and player.y<=crate.y+crate.size):
            print("crate collision")

        #else:
         #   print("no crate collision")
        

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
        #pygame.draw.rect(display, RED, b.rect)

def updateBullets():
    for b in bullets:
        b.y += b.ySpeed
        b.x += b.xSpeed

        if 0 >= b.x or WIDTH <= b.x:
            bullets.remove(b)

        if 0 >= b.y or HEIGHT <= b.y:
            bullets.remove(b)

def checkCollisions():
    for b in bullets:
        for z in zombieList:
            #print(bullets)
            if (b.x>=z.x-scrollX+30 and b.x<=(z.x+70-scrollX)) and (b.y>=z.y-scrollY+10 and b.y<=(z.y+70-scrollY)):
            #if z.rect.colliderect(b.rect):
                print('hit')
                z.hp -= 5
                bullets.remove(b)

                if len(bullets) <= 1:
                    print(",,,,,,,,,,,,,,,,,,,,")
                    break
                
def healthBar():
    pygame.draw.rect(display, RED, (100,HEIGHT-100,400,30))
    pygame.draw.rect(display, neonGreen, (100,HEIGHT-100,player.hp,30))

def levelBar():
    levelProgress = (player.levelProgress/zombieLevelSpawn[player.level])*400
    if levelProgress > 400:
        levelProgress = 400
    pygame.draw.rect(display, WHITE, (100,HEIGHT-50,400,20))
    pygame.draw.rect(display, BLACK, (100,HEIGHT-50,levelProgress,20))

    if player.levelProgress == zombieLevelSpawn[player.level]:
        player.levelProgress = 0
        player.level += 1

def zombieHit():
    for z in zombieList:
        if (player.x>=z.x-scrollX+30 and player.x<=(z.x+70-scrollX)) and (player.y>=z.y-scrollY+10 and player.y<=(z.y+70-scrollY)) and z.reachCheck == True:
            player.hp -= z.damage
            z.reachCheck = False

def drawStats():
    pass

def bulletTracker():
    graphics2 = font2.render(str(bulletsLeft), 1, BLACK)
    graphics3 = font2.render(str(totalAmmo), 1, BLACK)
    display.blit(graphics2, (100, 550))
    display.blit(graphics3, (155, 550))
    pygame.draw.line(display, BLACK, (145,HEIGHT-150), (145,HEIGHT-120), 1)

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
player = Player((WIDTH/2)-35, (HEIGHT/2)-35)
#player = Player(0, 0, 71, 71, 100, playerColour, 0, 0)
playerSpeed = 5 * frameRateMultiplier
zombieSpeed = 1.5 * frameRateMultiplier

zombieLevelHP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
zombieLevelSpawn = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
zombieLevelDamage = [100, 10, 15, 20, 25, 25, 30, 35, 40, 45, 45, 50, 60]

crosshair = Crosshair()

# create random coordinates for crate placement
crateX = []
crateY = []
crateSize = []
for i in range(100):
    crateX.append(randint(10, 3900))
    crateY.append(randint(10, 3900))
    crateSize.append(randint(50, 150))

crates = []
for i in range(100):
    crates.append(Crate(crateX[i], crateY[i], crateSize[i]))

# random zombie x, y spawns
zombieX = []
zombieY = []
for i in range(200):
    zombieX.append(randint(1000, 4000))
    zombieY.append(randint(350, 4000))

# create list of zombies
zombieList = []
for i in range(zombieLevelSpawn[player.level]):
    zombieList.append(Zombie(zombieX[i], zombieY[i], zombieLevelHP[player.level], zombieLevelDamage[player.level]))

# list for bullets
bullets = []

# list of guns
waterGun = Gun(player.x+20, player.y+20, "water gun.png")

guns = [waterGun]

# list of mag size
totalAmmo = 60
bulletsLeft = 30
magSize = 30

# ---------------------------------------#
# main program                           #
# ---------------------------------------#
while inPlay:
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

    if keys[pygame.K_r] and totalAmmo != 0:
        if bulletsLeft != magSize:
            totalAmmo = totalAmmo - (magSize-bulletsLeft)
            if totalAmmo <= 0:
                bulletsLeft += abs(totalAmmo)
                totalAmmo = 0
            
            else:
                bulletsLeft = magSize   

    # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # shoots gun on left click
        if event.type == pygame.MOUSEBUTTONDOWN and bulletsLeft != 0: 
            bullets.append(Bullets(player.x+30, player.y+30, 1))

            player.hp -= 1

            if bulletsLeft != 0:
                bulletsLeft -= 1
            
            else:
                bulletsLeft = 0

    #------------------------------------------------#
    if player.hp <= 0:
        gameEnd = True

    redrawGameWindow()

    #-----------------------#

#---------------------------------------#
pygame.quit()
