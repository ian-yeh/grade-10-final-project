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
BEGIN = pygame.time.get_ticks()
WIDTH = 1536
HEIGHT = 864

display = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255) 
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)
RED = (250, 0, 0)
YELLOW = (237, 219, 78)
grass = (98, 189, 98)
neonGreen = (57, 255, 20)
BORDER = (140, 140, 140)

shopInterface = (140, 99, 65)

outline = 0

font = pygame.font.Font('CaviarDreams.ttf', 15)
font2 = pygame.font.Font("CaviarDreams.ttf", 30)
font3 = pygame.font.Font("CaviarDreams.ttf", 35)

inPlay = True
gameEnd = ""

scrollX = 0
scrollY = 0

frameRateMultiplier = 1.5

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
        
        self.xSpeed = bulletSpeed*frameRateMultiplier * math.cos(self.angle)
        self.ySpeed = bulletSpeed*frameRateMultiplier * math.sin(self.angle)

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

        self.hp = 500

        self.level = 0
        self.levelProgress = 0

        # count bullets
        self.count = 0

        self.rect = pygame.Rect(self.x, self.y, 70,70)
        self.spriteOrg = pygame.image.load("playerAnimation1.png")

        

    def show(self, screen):
        self.mouseCoords = pygame.mouse.get_pos()
        
        if self.mouseCoords[0] >= WIDTH/2:
            self.sprite = pygame.transform.scale(self.spriteOrg, (70, 70))
            
        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(self.spriteOrg, (70, 70)), True, False)

        
        
        display.blit(self.sprite, (self.x, self.y))

        # draw player hitbox
        #pygame.draw.rect(display, RED, self.rect, 1)

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
    
    reloadAnimation()
    reloadInstructions()
    
    healthBar()
    levelBar()

    drawBullets()
    checkCollisions()
    updateBullets()
    bulletTracker()
    drawCoinTracker()

    zombieHit()

    drawStats()
    drawTime()

    playerInvincible()

    drawShop()
    drawCrosshair()
    
    if gameEnd == "lose":
        pygame.mouse.set_visible(True)
        loseScreen()

    if gameEnd == "win":
        pygame.mouse.set_visible(True)
        winScreen()

    clock.tick(60)
    pygame.display.update()

def loseScreen():
    display.blit(pygame.image.load("lose screen.png"), (0,0))

def winScreen():
    display.fill((WHITE))

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
            player.money += 1000000

            zombieHit1.play()

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


        shopRect = pygame.Rect(1600-scrollX, 980-scrollY, 200, 150)
        if crateRect.colliderect(shopRect): 
            crates.remove(crate)

def drawMap():
    global scrollX
    global scrollY
    # set colour for grass
    display.fill(BORDER)
    # set border
    pygame.draw.rect(display, grass, (0-scrollX, 0-scrollY, 4000,4000))   
    #map = pygame.image.load("map.jpg")
    #display.blit(map, (0-scrollX, 0-scrollY)) 

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

#Animation Images#  
animationScaleFactor = 40
reloadAnimation1 = pygame.transform.scale(pygame.image.load("reload1.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation2 = pygame.transform.scale(pygame.image.load("reload2.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation3 = pygame.transform.scale(pygame.image.load("reload3.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation4 = pygame.transform.scale(pygame.image.load("reload4.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation5 = pygame.transform.scale(pygame.image.load("reload5.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation6 = pygame.transform.scale(pygame.image.load("reload6.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation7 = pygame.transform.scale(pygame.image.load("reload7.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation8 = pygame.transform.scale(pygame.image.load("reload8.png"), (animationScaleFactor, animationScaleFactor))
reloadAnimation9 = pygame.transform.scale(pygame.image.load("reload9.png"), (animationScaleFactor, animationScaleFactor))

reload_Imgs = [reloadAnimation1, reloadAnimation2, reloadAnimation3, reloadAnimation4, reloadAnimation5, reloadAnimation6, reloadAnimation7, reloadAnimation8, reloadAnimation9]
animationCount = 0
loopCount = 0
pressedReload = False
joe = False
def reloadAnimation():
    global loopCount
    global animationCount
    global pressedReload
    global joe
    if (pressedReload or joe):
        joe = True
        if animationCount + 1 >= 27:
            animationCount = 0 
        animationCount += 1
        display.blit(reload_Imgs[animationCount//3], ((WIDTH/2)-30, (HEIGHT/2)-30))
        if reload_Imgs[animationCount//3] == reloadAnimation9:
            pressedReload = False
            joe = False
            animationCount = 0 

def reloadInstructions():
    global bulletsLeft
    global pressedReload
    if bulletsLeft == 0 and not pressedReload:
        graphics = font.render("Press R to reload", 1, BLACK) 
        display.blit(graphics, (500,300))        

def drawGun():
    currentGun.show()

def drawBullets():
    for b in bullets:
        display.blit(b.bullet, (b.x, b.y))

def updateBullets():
    if currentGun == guns[0] or currentGun == guns[1]:
        for b in bullets:
            b.x += b.xSpeed
            b.y += b.ySpeed

            if 0 >= b.x or WIDTH <= b.x:
                if b in bullets:
                    bullets.remove(b)

            if 0 >= b.y or HEIGHT <= b.y:
                if b in bullets:
                    bullets.remove(b)

    if currentGun == guns[2] and bullets != []:
        count = 0
        for b in bullets:
            count += 1
            if count % 3 == 0:
                b.x += b.xSpeed
                b.y += b.ySpeed

            if count % 3 == 1:
                b.x += b.xSpeed+2
                b.y += b.ySpeed+2

            if count % 3 == 2:
                b.x += b.xSpeed-2
                b.y += b.ySpeed-2

            if 0 >= b.x or WIDTH <= b.x:
                if b in bullets:
                    bullets.remove(b)

            if 0 >= b.y or HEIGHT <= b.y:
                if b in bullets:
                    bullets.remove(b)

    if currentGun == guns[3] and bullets != []:
        count2 = 0
        for b in bullets:
            count2 += 1
            if count2 % 5 == 0:
                b.x += b.xSpeed
                b.y += b.ySpeed

            if count2 % 5 == 1:
                b.x += b.xSpeed+2
                b.y += b.ySpeed+2

            if count2 % 5 == 2:
                b.x += b.xSpeed-2
                b.y += b.ySpeed-2

            if count2 % 5 == 3:
                b.x += b.xSpeed-5
                b.y += b.ySpeed-5

            if count2 % 5 == 4:
                b.x += b.xSpeed+5
                b.y += b.ySpeed+5

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
            graphics = font3.render("F", 1, BLACK)
            display.blit(graphics, (i.x-scrollX+80, i.y-scrollY-16))

            if addBullet == True:
                totalAmmo += 30
                bulletPatchList.remove(i)   

    if len(bulletPatchList) < 10:
        bulletPatchList.append(Ammo(randint(10, 3900), randint(10, 3900), 10))    

def drawCoinTracker():
    coinImg = pygame.image.load("Coin.png")
    newcoinImg = pygame.transform.scale(coinImg, (50, 50))
    display.blit(newcoinImg, (10,15))
    moneyText = font3.render(str(player.money), 1, BLACK)
    display.blit(moneyText, (73, 18))     

def checkCollisions():
    global missedShots

    for b in bullets:
        bRect = pygame.Rect(b.x, b.y, 5, 5)
        for z in zombieList:
            zRect = pygame.Rect(z.x-scrollX, z.y-scrollY, 70, 70)
            
            if zRect.colliderect(bRect) and (currentGun==guns[0] or currentGun==guns[2]):
                print("hit")
                missedShots = 0
                z.hp -= 5*damageMultiplier

                if b in bullets:
                    bullets.remove(b)
                
            if zRect.colliderect(bRect) and (currentGun==guns[1] or currentGun==guns[3]):
                missedShots = 0
                print("hit")
                z.hp -= 10*damageMultiplier

                if b in bullets:
                    bullets.remove(b)

    for b in bullets:
        bRect = pygame.Rect(b.x, b.y, 10, 10)
        for crate in crates:
            crateRect = pygame.Rect((crate.x-5)-scrollX, (crate.y-5)-scrollY, crate.size+10, crate.size+10)
            
            if bRect.colliderect(crateRect):
                if b in bullets:
                    bullets.remove(b)
            
def healthBar():
    pygame.draw.rect(display, RED, (70,HEIGHT-100,400,30))
    pygame.draw.rect(display, neonGreen, (70,HEIGHT-100,(player.hp/currentHealth)*400,30))

def levelBar():
    levelProgress = (player.levelProgress/zombieLevelSpawn[player.level])*400
    
    levelText = "Level " + str(player.level + 1)

    if levelProgress > 400:
        levelProgress = 400

    pygame.draw.rect(display, WHITE, (70,HEIGHT-50,400,20))
    pygame.draw.rect(display, BLACK, (70,HEIGHT-50,levelProgress,20))

    graphics = font.render(levelText, 1, RED)
    display.blit(graphics, (350, HEIGHT-50))

    if player.levelProgress == zombieLevelSpawn[player.level]:
        hooray.play()

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

    # display coordinates
    playerCoords = [round(scrollX), round(scrollY)]
    showCoordinates = font2.render("[x, y] = " + str(playerCoords), 1, BLACK)
    display.blit(showCoordinates, (70, HEIGHT-200))

    # display kill count
    killCount = font2.render("Kills: " + str(player.killCount), 1, BLACK)
    display.blit(killCount, (70, HEIGHT-250))

def drawTime():
    global elapsed
    elapsed = pygame.time.get_ticks() - BEGIN
    minutesPassed = int(elapsed / (1000 * 60))
    secondsPassed = int((elapsed / 1000) % 60)
    millisecondsPassed = int((elapsed % 1000) / 10)
    timer = font3.render(f"{minutesPassed:2d}:{secondsPassed:2d}:{millisecondsPassed:3d}", True,(0, 0, 0))
    display.blit(timer, (WIDTH-180, 20))

def bulletTracker():
    graphics2 = font2.render(str(bulletsLeft), 1, BLACK)
    graphics3 = font2.render(str(totalAmmo), 1, BLACK)
    display.blit(graphics2, (70, HEIGHT-150))
    display.blit(graphics3, (125, HEIGHT-150))
    pygame.draw.line(display, BLACK, (115,HEIGHT-150), (115,HEIGHT-120), 1)

def drawShop():
    global inShop, gunPressed, itemPressed, inShop1, inShop2

    shop = pygame.image.load("shop.png")
    shopRect = pygame.Rect(1600-scrollX, 980-scrollY, 200, 150)
    display.blit(shop, (1600-scrollX, 980-scrollY))   

    if player.rect.colliderect(shopRect):
        inShop = True

        for z in zombieList:
            z.speed = 0
            z.damage = 0
        pygame.draw.rect(display, YELLOW, shopRect, 3)
        display.blit(pygame.image.load("shopInterface.png"), (200, 150))

        pos = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(pos[0], pos[1], 1, 1)

        # guns panel
        rect1 = pygame.Rect(308, 341, 185, 116) # Spritz
        rect2 = pygame.Rect(518, 341, 185, 116) # super soaker
        rect3 = pygame.Rect(308, 494, 185, 116) # splash
        rect4 = pygame.Rect(518, 494, 185, 116) # the wetter

        # items panel
        rect5 = pygame.Rect(844, 341, 185, 116) # health
        rect6 = pygame.Rect(1054, 341, 185, 116) # invincibility
        rect7 = pygame.Rect(844, 494, 185, 116) # speed boost
        rect8 = pygame.Rect(1054, 494, 185, 116) # medkit

        rect9 = pygame.Rect(308, 341, 185, 116) # Spritz
        rect10 = pygame.Rect(518, 341, 185, 116) # super soaker
        rect11 = pygame.Rect(308, 494, 185, 116) # splash

        nextButton = pygame.Rect(1074, 162, 180, 50)
        
        backButton = pygame.Rect(1074, 162, 180, 50)

        if inShop1:
            if mouseRect.colliderect(rect1):
                pygame.draw.rect(display, YELLOW, rect1, 5)
                gunPressed = "Spritz"

            if mouseRect.colliderect(rect2):
                pygame.draw.rect(display, YELLOW, rect2, 5)
                gunPressed = "Super Soaker"

            if mouseRect.colliderect(rect3):
                pygame.draw.rect(display, YELLOW, rect3, 5)
                gunPressed = "Splash"

            if mouseRect.colliderect(rect4):
                pygame.draw.rect(display, YELLOW, rect4, 5)
                gunPressed = "Wetter"

            if mouseRect.colliderect(rect5):
                pygame.draw.rect(display, YELLOW, rect5, 5)
                itemPressed = "health"

            if mouseRect.colliderect(rect6):
                pygame.draw.rect(display, YELLOW, rect6, 5)
                itemPressed = "invincibility"

            if mouseRect.colliderect(rect7):
                pygame.draw.rect(display, YELLOW, rect7, 5)
                itemPressed = "speed"

            if mouseRect.colliderect(rect8):
                pygame.draw.rect(display, YELLOW, rect8, 5)
                itemPressed = "medkit"

            if mouseRect.colliderect(nextButton):
                itemPressed = "nextButton"
                pygame.draw.rect(display, YELLOW, nextButton, 5)
                

        if inShop2:
            display.blit(pygame.image.load("shopInterface2.png"), (200, 150))

            if mouseRect.colliderect(rect9):
                pygame.draw.rect(display, YELLOW, rect9, 5)
                itemPressed = "bullet speed"

            if mouseRect.colliderect(rect10):
                pygame.draw.rect(display, YELLOW, rect10, 5)
                itemPressed = "double damage"

            if mouseRect.colliderect(rect11):
                pygame.draw.rect(display, YELLOW, rect11, 5)
                itemPressed = "add health"

            if mouseRect.colliderect(backButton):
                itemPressed = "backButton"
                pygame.draw.rect(display, YELLOW, backButton, 5)

    else:
        for z in zombieList:
            z.speed = zombieSpeedList[player.level]
            if not invincible:
                z.damage = zombieLevelDamage[player.level]

        inShop = False

def playerInvincible():
    global startTime
    #print(elapsed, startTime)

    if invincible:
        player.spriteOrg = pygame.image.load("invincibility.png")

        for z in zombieList:
            z.damage = 0

        if elapsed-startTime > 30000:
            
            for z in zombieList:
                z.damage = zombieLevelDamage[player.level]

            invicible = False
            startTime = 0

            player.spriteOrg = pygame.image.load("playerAnimation1.png")

# ---------------------------------------#
# variables                             #
# ---------------------------------------#
inShop = False
inShop1 = True
inShop2 = False

player = Player((WIDTH/2)-35, (HEIGHT/2)-35)
playerSpeed = 5 * frameRateMultiplier

zombieSpeedList = [1.5*frameRateMultiplier, 1.75*frameRateMultiplier, 2*frameRateMultiplier, 2.25*frameRateMultiplier, 2.5*frameRateMultiplier, 2.75*frameRateMultiplier, 3*frameRateMultiplier, 3.25*frameRateMultiplier, 3.5*frameRateMultiplier, 3.75*frameRateMultiplier, 4*frameRateMultiplier, 4.5*frameRateMultiplier, 5*frameRateMultiplier, 5.5*frameRateMultiplier, 5.75*frameRateMultiplier, 6*frameRateMultiplier, 6.25*frameRateMultiplier, 6.5*frameRateMultiplier, 7*frameRateMultiplier, 1000]
zombieLevelHP = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110, 120, 1000]
zombieLevelSpawn = [10, 15, 15, 20, 20, 30, 35, 35, 35, 35, 40, 45, 50, 60, 70, 80, 90, 100, 120, 130, 1000]
zombieLevelDamage = [20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 75, 80, 85, 90, 100, 110, 120, 130, 140, 150, 1000]

crosshair = Crosshair()

bulletSpeed = 14

# create random coordinates for crate placement
crateX = []
crateY = []
crateSize = []
for i in range(85):
    crateX.append(randint(10, 3900))
    crateY.append(randint(10, 3900))
    crateSize.append(randint(50, 150))

crates = []
for i in range(85):
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
splash = Gun(player.x+15, player.y+15, "splash.png")
theWetter = Gun(player.x+5, player.y+5, "the wetter.png")

damageMultiplier = 1

guns = [waterGun, superSoaker, splash, theWetter]
currentGun = guns[0]

gunPressed = ""
itemPressed = ""

# list of mag size
totalAmmo = 60
bulletsLeft = 30
magSize = 30

keysPressed = 0

pressedReload = False

invincible = False

startTime = 0
elapsed = 0

missedShots = 0

currentHealth = 500

# sounds
pewSound = pygame.mixer.Sound("classicShot.wav")
hooray = pygame.mixer.Sound("hooray.wav")
reloading = pygame.mixer.Sound("reloading.wav")

zombieHit1 = pygame.mixer.Sound("zombieHit1.wav")

imInvincible = pygame.mixer.Sound("imInvincible.wav")

walking = pygame.mixer.Sound("mcWalk.mp3")

aimBad = pygame.mixer.Sound("aimBad.wav")

# ---------------------------------------#
# main program                           #
# ---------------------------------------#
startScreen = pygame.image.load("Home Screen 1.png")
startScreen2 = pygame.image.load("Home Screen 2.png")
startScreen3 = pygame.image.load("Home Screen 3.png")
controlScreen = pygame.image.load("Controls Screen.png")
startMenu = True
bob = False
count = 0

while startMenu:
    mousePosition = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if mousePosition[0] >= 361 and mousePosition[1] >= 307 and mousePosition[0] <= 831 and mousePosition[1] <= 396:
            if not bob:
                display.blit(startScreen2, (0,0))
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    startMenu = False
        elif (mousePosition[0] >= 361 and mousePosition[1] >= 438 and mousePosition[0] <= 831 and mousePosition[1] <= 528) or bob:
            if not bob:
                display.blit(startScreen3, (0,0))
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN or bob:
                bob = True
                display.blit(controlScreen, (0,0))
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Joe")
                if mousePosition[0] <= 1137 and mousePosition[1] <= 149 and mousePosition[0] >= 1038 and mousePosition[1] >= 41:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        bob = False
                      #  print("Joe")
        elif not bob:
            display.blit(startScreen, (0,0))
            pygame.display.update()

while inPlay:
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
            reloading.play()

            pressedReload = True
            totalAmmo = totalAmmo - (magSize-bulletsLeft)
            if totalAmmo <= 0:
                bulletsLeft += totalAmmo+(magSize-bulletsLeft)
                totalAmmo = 0
        
            else:
                bulletsLeft = magSize    
    
    if keys[pygame.K_f]: 
        addBullet = True
    
    else:
        addBullet = False

    # processing KEYDOWN events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if not inShop:

            # shoots gun on left click
            if event.type == pygame.MOUSEBUTTONDOWN and bulletsLeft != 0: # and event.button == 1: 
                
                missedShots += 1
                #print(missedShots)
                pewSound.play()
                if currentGun == guns[0] or currentGun == guns[1]:
                    bullets.append(Bullets(player.x+30, player.y+30, 1))    

                    if bulletsLeft > 0:
                        bulletsLeft -= 1
                    
                    else:
                        bulletsLeft = 0

                if currentGun == guns[2]:
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))

                    if bulletsLeft > 0:
                        bulletsLeft -= 3
                    
                    else:
                        bulletsLeft = 0

                if currentGun == guns[3]:
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))
                    bullets.append(Bullets(player.x+30, player.y+30, 1))

                    if bulletsLeft > 0:
                        bulletsLeft -= 5
                    
                    else:
                        bulletsLeft = 0

        if inShop:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gunPressed == "Spritz":
                    currentGun = guns[0]

                if gunPressed == "Super Soaker":
                    if player.money - 4000 >= 0:
                        player.money -= 4000
                        currentGun = guns[1]

                if gunPressed == "Splash":
                    if player.money - 6000 >= 0:
                        player.money -= 6000
                        currentGun = guns[2]

                if gunPressed == "Wetter":
                    
                    if player.money - 10000 >= 0:
                        player.money -= 10000
                        currentGun = guns[3]

                if itemPressed == "health":

                    if player.money - 500 >= 0:

                        if player.hp + 50 > currentHealth:
                            player.hp = currentHealth

                        else:
                            player.hp += 75

                        player.money -= 50

                if itemPressed == "invincibility":
        
                    if player.money - 3500 >= 0:
                        imInvincible.play()

                        startTime = pygame.time.get_ticks()
                        invincible = True
                        player.money -= 3500

                if itemPressed == "speed":
                    if player.money - 2500 >= 0:
                        playerSpeed += 3

                        player.money -= 2500

                if itemPressed == "medkit":
                    if player.money - 4000 >= 0:
                        player.hp = currentHealth

                        player.money -= 4000

                if itemPressed == "bullet speed":
        
                    if player.money - 10000 >= 0:
                        bulletSpeed += 4
                        player.money -= 10000

                if itemPressed == "double damage":
                    if player.money - 15000 >= 0:
                        damageMultiplier *= 2

                        player.money -= 15000

                if itemPressed == "add health":
                    if player.money - 8000 >= 0:
                        currentHealth += 200

                        player.money -= 8000

                if itemPressed == "nextButton":
                    inShop1 = False
                    inShop2 = True

                if itemPressed == "backButton":
                    inShop1 = True
                    inShop2 = False
        itemPressed = ""
        gunPressed = ""  

    print(player.hp, currentHealth)
    #------------------------------------------------#
    if player.hp <= 0:
        gameEnd = "lose"

    if player.level == 19:
        gameEnd = "win"

    if missedShots >= 7:
        aimBad.play()
        missedShots = 0

    redrawGameWindow()

    #-----------------------#

#---------------------------------------#
pygame.quit() 
