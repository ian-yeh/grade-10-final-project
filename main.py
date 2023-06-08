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
WIDTH = 1536
HEIGHT = 864

display = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255) 
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (250, 0, 0)
grass = (98, 189, 98)
neonGreen = (57, 255, 20)
BORDER = (140, 140, 140)

outline = 0

font = pygame.font.Font('CaviarDreams.ttf', 15)
font2 = pygame.font.Font("CaviarDreams.ttf", 30)
font3 = pygame.font.Font("CaviarDreams.ttf", 35)

inPlay = True
gameEnd = False

scrollX = 0
scrollY = 0

frameRateMultiplier = 2.5

# ---------------------------------------#
# ---------------------------------------#
class Ammo:
    def __init__(self, x, y, bulletNumber):
        self.x = x
        self.y = y
        self.bulletNumber = bulletNumber
        self.load = pygame.image.load("bulletPatch.png")
    
    def show(self):
        self.sprite = pygame.transform.scale(self.load, (80, 80))
        display.blit(self.sprite, (self.x-scrollX, self.y-scrollY))
        
class Crate:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.rect = pygame.Rect(self.x-scrollX, self.y-scrollY, self.size, self.size)

        

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

        
        self.image = pygame.image.load(picture)
        #self.image.set_colorkey(WHITE)

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

        self.mouseCoords = pygame.mouse.get_pos()
        self.xDisplace = self.mouseCoords[0] - self.x
        self.yDisplace = self.mouseCoords[1] - self.y
        
        self.angle = math.radians(math.degrees(math.atan2(self.yDisplace, self.xDisplace)))
        
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

        self.rect = pygame.Rect(self.x, self.y, 70,70)

    def show(self, screen):
        self.mouseCoords = pygame.mouse.get_pos()
        self.spriteOrg = pygame.image.load("playerAnimation1.png")

        
        if self.mouseCoords[0] >= WIDTH/2:
            self.sprite = pygame.transform.scale(self.spriteOrg, (70, 70))
            
        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(self.spriteOrg, (70, 70)), True, False)

        
        
        display.blit(self.sprite, (self.x, self.y))
        pygame.draw.rect(display, RED, self.rect, 1)

class Zombie:
    def __init__(self, x, y, hp, damage, speed):
        self.x = x
        self.y = y 

        self.hp = hp   

        self.damage = damage
        self.speed = speed

        self.image = pygame.image.load("zombie.png")
        self.sprite = pygame.transform.scale(self.image, (120, 120))

        self.reachCheck = False
        self.checkPointX = choice(range(200, 1000, 2))
        self.checkPointY = choice(range(100, 600, 2))

    def show(self): #draws zombie
        if self.reachCheck == False:
            # moves zombie based on position compared to player
            if self.checkPointX > self.x-scrollX: #player is to right
                self.x += self.speed

            if self.checkPointX < self.x-scrollX: # player is to sleft
                self.x -= self.speed

            if self.checkPointY > self.y-scrollY: # player is below zombie
                self.y += self.speed

            if self.checkPointY < self.y-scrollY: # player is above zombie
                self.y -= self.speed

            if -self.speed <= (self.x-self.checkPointX-scrollX) <= self.speed and -self.speed <= (self.y-self.checkPointY-scrollY) <= self.speed:
                self.reachCheck = True
                self.checkPointX = choice(range(round(player.x-50), round(player.x+70), 2))
                self.checkPointY = choice(range(round(player.y-50), round(player.y+70), 2))

        elif self.reachCheck == True:
            # moves zombie based on position compared to player
            if player.x-30 > self.x-scrollX: #player is to right
                self.x += self.speed

            if player.x-30 < self.x-scrollX: # player is to left
                self.x -= self.speed

            if player.y-30 > self.y-scrollY: # player is below zombie
                self.y += self.speed

            if player.y-30 < self.y-scrollY: # player is above zombie
                self.y -= self.speed

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
    drawBulletPatch()
    drawCrates()
    drawPlayer()
    drawZombies()
    drawGun()

    healthBar()
    levelBar()

    drawBullets()
    checkCollisions()
    updateBullets()
    bulletTracker()
    drawCoinTracker()

    zombieHit()

    drawCrosshair()

    drawStats()
    
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
            player.money += 100

def drawCrates():
    global crateRect
    global scrollX
    global scrollY
    for crate in crates:
        crate.show()
        crateRect = pygame.Rect((crate.x-5)-scrollX, (crate.y-5)-scrollY, crate.size+10, crate.size+10)
        #pygame.draw.rect(display, RED, crateRect, 1)
         
        collisionTolerance = 15
        if player.rect.colliderect(crateRect): 
        
            if abs(crateRect.top - player.rect.bottom) < collisionTolerance: # collision with top of crate
                scrollY -= playerSpeed

            if abs(crateRect.bottom - player.rect.top) < collisionTolerance: # collision with bottom of crate
                scrollY += playerSpeed
        
            if abs(crateRect.right - player.rect.left) < collisionTolerance: # collision with left of crate
                scrollX += playerSpeed

            if abs(crateRect.left - player.rect.right) < collisionTolerance: #collision with right of crate
                scrollX -= playerSpeed     

def drawMap():
    global scrollX
    global scrollY
    # set colour for grass
    display.fill(BORDER)
    # set border
    pygame.draw.rect(display, grass, (0-scrollX, 0-scrollY, 4000,4000))    

    # set border sides
    topSideRect = pygame.Rect(0-scrollX, -100-scrollY, 4000,100)
    bottomSideRect = pygame.Rect(0-scrollX, 4000-scrollY, 4000, 100)
    leftSideRect = pygame.Rect(-100-scrollX, 0-scrollY, 100, 4000)
    rightSideRect = pygame.Rect(4000-scrollX, 0-scrollY, 100, 4000)

    # top side
    pygame.draw.rect(display, BORDER, topSideRect,)  
    # bottom side
    pygame.draw.rect(display, BORDER, bottomSideRect)      
    # left side
    pygame.draw.rect(display, BORDER, leftSideRect)    
    # right side
    pygame.draw.rect(display, BORDER, rightSideRect)

    # check if player is off map
    if player.rect.colliderect(topSideRect):
        scrollY += playerSpeed    

    if player.rect.colliderect(bottomSideRect):
        scrollY -= playerSpeed  

    if player.rect.colliderect(rightSideRect):
        scrollX -= playerSpeed    

    if player.rect.colliderect(leftSideRect):
        scrollX += playerSpeed      

def drawGun():
    currentGun.show()

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
            if b in bullets:
                bullets.remove(b)

        if 0 >= b.y or HEIGHT <= b.y:
            if b in bullets:
                bullets.remove(b)

addBullet = False
def drawBulletPatch():
    global totalAmmo
    global addBullet
    for i in range(len(bulletPatchList)):
        bulletPatchList[i].show()
    for i in bulletPatchList:
        if (player.x>i.x-scrollX-60 and player.x<i.x-scrollX+70 and player.y>i.y-scrollY-60 and player.y<i.y-scrollY+70):
            pygame.draw.circle(display,BLACK, (i.x-scrollX+40, i.y-scrollY+40), 60, 1)
            pygame.draw.rect(display, BLACK, (i.x-scrollX+70, i.y-scrollY-15, 40, 40), 1)
            pygame.draw.rect(display, grass, (i.x-scrollX+71, i.y-scrollY-14, 38,38))
            graphics = font3.render("E", 1, BLACK)
            display.blit(graphics, (i.x-scrollX+80, i.y-scrollY-16))

            if addBullet == True:
                totalAmmo += 30
                bulletPatchList.remove(i)   

    if len(bulletPatchList) < 10:
        bulletPatchList.append(Ammo(randint(10, 3900), randint(10, 3900), 10))    

def drawCoinTracker():
    coinImg = pygame.image.load("Coin.png")
    newcoinImg = pygame.transform.scale(coinImg, (20, 20))
    display.blit(newcoinImg, (10,15))
    moneyText = font.render(str(player.money), 1, BLACK)
    display.blit(moneyText, (40, 17))     

def checkCollisions():
    global zombieCollide
    for b in bullets:
        bRect = pygame.Rect(b.x, b.y, 5, 5)
        for z in zombieList:
            zRect = pygame.Rect(z.x-scrollX, z.y-scrollY, 70, 70)
            
            if zRect.colliderect(bRect):
                print("hit")
                z.hp -= 5

                if b in bullets:
                    bullets.remove(b)

    for b in bullets:
        bRect = pygame.Rect(b.x, b.y, 10, 10)
        for crate in crates:
            crateRect = pygame.Rect((crate.x-5)-scrollX, (crate.y-5)-scrollY, crate.size+10, crate.size+10)
            
            if bRect.colliderect(crateRect):
                if b in bullets:
                    bullets.remove(b)

    for z in zombieList:
        zRect = pygame.Rect(z.x-scrollX, z.y-scrollY, 70, 70)
        for crate in crates:
            crateRect = pygame.Rect((crate.x-5)-scrollX, (crate.y-5)-scrollY, crate.size+10, crate.size+10)
            
            if zRect.colliderect(crateRect):
                zombieCollide = True
            
def healthBar():
    pygame.draw.rect(display, RED, (100,HEIGHT-100,400,30))
    pygame.draw.rect(display, neonGreen, (100,HEIGHT-100,player.hp,30))

def levelBar():
    levelProgress = (player.levelProgress/zombieLevelSpawn[player.level])*400
    
    levelText = "Level " + str(player.level + 1)

    if levelProgress > 400:
        levelProgress = 400

    pygame.draw.rect(display, WHITE, (100,HEIGHT-50,400,20))
    pygame.draw.rect(display, BLACK, (100,HEIGHT-50,levelProgress,20))

    graphics = font.render(levelText, 1, BLACK)
    display.blit(graphics, (350, HEIGHT-50))

    if player.levelProgress == zombieLevelSpawn[player.level]:
        player.levelProgress = 0
        player.level += 1
        zombieList.clear()

        for i in range(zombieLevelSpawn[player.level]):
            zombieList.append(Zombie(zombieX[i], zombieY[i], zombieLevelHP[player.level], zombieLevelDamage[player.level], zombieSpeedList[player.level]))

def zombieHit():
    for z in zombieList:
        if (player.x>=z.x-scrollX+30 and player.x<=(z.x+70-scrollX)) and (player.y>=z.y-scrollY+10 and player.y<=(z.y+70-scrollY)) and z.reachCheck == True:
            player.hp -= z.damage
            z.reachCheck = False

def drawStats():
    playerCoords = [round(scrollX), round(scrollY)]
    showCoordinates = font3.render("[x, y] = " + str(playerCoords), 1, BLACK)
    display.blit(showCoordinates, (200, 200))

def bulletTracker():
    graphics2 = font2.render(str(bulletsLeft), 1, BLACK)
    graphics3 = font2.render(str(totalAmmo), 1, BLACK)
    display.blit(graphics2, (100, HEIGHT-150))
    display.blit(graphics3, (155, HEIGHT-150))
    pygame.draw.line(display, BLACK, (145,HEIGHT-150), (145,HEIGHT-120), 1)

def drawShop():
    pass   

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
player = Player((WIDTH/2)-35, (HEIGHT/2)-35)
playerSpeed = 5 * frameRateMultiplier

# create boolean value for zombie crashing into crate
zombieCollide = False

zombieSpeedList = [1.5*frameRateMultiplier, 1.75*frameRateMultiplier, 2*frameRateMultiplier, 2.25*frameRateMultiplier, 2.5*frameRateMultiplier, 2.75*frameRateMultiplier, 3, 3.25*frameRateMultiplier, 3.5*frameRateMultiplier, 3.75*frameRateMultiplier, 4*frameRateMultiplier]
zombieLevelHP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
zombieLevelSpawn = [10, 15, 15, 20, 20, 30, 35, 35, 35, 35, 40, 45, 50]
zombieLevelDamage = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 85]

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
    zombieList.append(Zombie(zombieX[i], zombieY[i], zombieLevelHP[player.level], zombieLevelDamage[player.level], zombieSpeedList[player.level]))

# list for bullet patches
# Random Coordinates for bullets
bulletPatchX = []
bulletPatchY = []
for i in range(10):
    bulletPatchX.append(randint(10, 3900))
    bulletPatchY.append(randint(10, 3900))

bulletPatchList = [] 
for i in range(10):
    bulletPatchList.append(Ammo(bulletPatchX[i], bulletPatchY[i], 10))    

# list for bullets
bullets = []

# list of guns
waterGun = Gun(player.x+15, player.y+15, "water gun.png")
superSoaker = Gun(player.x+15, player.y+15, "super soaker.png")

guns = [waterGun, superSoaker]
currentGun = guns[0]

# list of mag size
totalAmmo = 60
bulletsLeft = 30
magSize = 30

keysPressed = 0

# ---------------------------------------#
# main program                           #
# ---------------------------------------#
while inPlay:
    keysPressed = 0
    #------move player-----#
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        inPlay = False
  
    #-----------check if player is in border----------#
    if keys[pygame.K_a]:
        scrollX -= playerSpeed

    if keys[pygame.K_d]:
        scrollX += playerSpeed 

    if keys[pygame.K_w]:
        scrollY -= playerSpeed

    if keys[pygame.K_s]:
        scrollY += playerSpeed  

    if keys[pygame.K_r] and totalAmmo != 0:
        if bulletsLeft != magSize:
            totalAmmo = totalAmmo - (magSize-bulletsLeft)
            if totalAmmo <= 0:
                bulletsLeft += totalAmmo+(magSize-bulletsLeft)
                totalAmmo = 0
    
            else:
                bulletsLeft = magSize
    
    if keys[pygame.K_e]: 
        addBullet = True
    
    else:
        addBullet = False

    # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # shoots gun on left click
        if event.type == pygame.MOUSEBUTTONDOWN and bulletsLeft != 0 and currentGun == guns[1] and event.button == 1: 
            bullets.append(Bullets(player.x+30, player.y+30, 1))    

            if bulletsLeft != 0:
                bulletsLeft -= 1
            
            else:
                bulletsLeft = 0

        # shoots gun on left click
        if event.type == pygame.MOUSEBUTTONDOWN and bulletsLeft != 0 and currentGun == guns[0] and event.button == 1: 
            bullets.append(Bullets(player.x+30, player.y+30, 1))

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
