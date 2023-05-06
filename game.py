# %% IMPORTS
import pygame as p
import math as m
import random
import numpy as np
import pandas as pd
from IPython.display import display
import layer 

# %% INITIAL VARS
# Switch between simulation and game mode
GAME_MODE = False    

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

# Screen parameters.
screenWidth = 700
screenHeight = 500

# Target parameters
targWidth = 20
targHeight = 30

maxTargets = 10                        

# Target control, percent chance of dropping bomb
launchBomb = 3

# Target move choices.
noMove = 0
left = -1
right = 1

# %% BULLET CLASS
class bullet:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.radius = 5
        self.heading = heading0
        self.velocity = 20
        self.exists = True
        self.hit = False
        return
    # init
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hit == False):
                if (GAME_MODE):
                    p.draw.circle(s, GREEN, [int(self.x), int(self.y)], self.radius, 1)
            else:
                self.explodeMe(s)
        return
    # drawMe
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    # moveMe
    
    def doIExist(self):
        return self.exists
    # doIExist
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return
    # explodeMe

# BULLET

# %% BOMB CLASS
class bomb:
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0
        self.radius = 7
        self.heading = 90
        self.velocity = 4
        self.exists = True
        self.hit = False
        return
    # init
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hit == False):
                if (GAME_MODE):
                    p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius, 0)
            else:
                self.explodeMe(s)
        return
    # draw me
    
    def moveMe(self):
        angRad = deg2Rad(self.heading)
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 0) and (bX < screenWidth))and((bY > 0) and (bY < screenHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    # moveMe
    
    def doIExist(self):
        return self.exists
    # doIExist
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 0)
            p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 0)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 0)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return
    # explodeMe

# BOMB

# %% TARGET CLASS
class target:
    def __init__(self, x0, y0, heading0):
        self.x = x0
        self.y = y0
        self.width = targWidth
        self.height = targHeight
        self.heading = heading0
        self.velocity = 1
        self.exists = True
        self.hitCount = 0
        self.directionInc = noMove
        self.moveSteps = 0
        return
    # init
    
    def getBombBay(self):
        bombBayX = self.x
        bombBayY = self.y + self.height
        return bombBayX, bombBayY
    # getBombBay
    
    def drawMe(self, s):
        if (self.exists == True):
            if (self.hitCount < 50):
                if (GAME_MODE):
                    p.draw.rect(s, RED, [self.x - self.width/2,self.y - self.height/2, self.width, self.height], 2)
            else:
                self.explodeMe(s)
        return
    # drawMe
    
    def explodeMe(self, s):
        if (GAME_MODE):
            p.draw.rect(s, YELLOW, [self.x - self.width/8, self.y - self.height/8, self.width/4, self.height/4], 2)
            p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], int(self.width/8), 1)
            p.draw.rect(s, ORANGE, [self.x - self.width/4, self.y - self.height/4, self.width/2, self.height/2], 2)
            p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], int(self.width/4), 1)
            p.draw.rect(s, GREEN, [self.x - self.width/2, self.y - self.height/2, self.width, self.height], 2)
            p.draw.circle(s, GREEN, [int(self.x), int(self.y)], int(self.width/2), 1)
            p.draw.rect(s, GREEN, [self.x - self.width, self.y - self.height, self.width*2, self.height*2], 2)
            p.draw.circle(s, GREEN, [int(self.x), int(self.y)], int(self.width * 2), 1)
        
        self.exists = False
        
        return
    #explodeMe
        
    def what2Do(self, closeTargX, targWidth, turretX, inc):
        myMove = noMove
        # Here we want to move left.
        if (turretX < self.x):
            if (closeTargX < self.x):
                if ((self.x - inc) > (closeTargX + targWidth)):
                    myMove = left
                else:
                    myMove = noMove
            else:
                myMove = left
        # No move.        
        elif (turretX == self.x):
            myMove = noMove
        # Move to the right.    
        elif (turretX > self.x):
            if (closeTargX > self.x):
                if ((self.x + inc) < (closeTargX - targWidth)):
                    myMove = right
                else:
                    myMove = noMove
            else:
                myMove = right
                
        return myMove
    # what2Do
        
    def moveMe(self, inc):
        self.x = self.x + inc
        if (self.x < self.width):  
            self.x = self.width
        elif (self.x > (screenWidth - self.width)):
            self.x = screenWidth - self.width
            
        return
    # moveMe
    
    def doIExist(self):
        return self.exists
    # doIExist

# TARGET

# %% TURRET CLASS
class turret:
   def __init__(self, x0, y0, rad0):
        self.x = x0
        self.y = y0
        self.exists = True
        self.hitCount = 0
        self.rad = rad0
        self.leftLimit = 3*rad0
        self.rightLimit = screenWidth - (3*rad0)
        self.gunLen = rad0*2
        self.gunAngle = 270
        self.gunTipX = 0
        self.gunTipY = 0      
        return
    # init
    
   def drawMe(self, s):
       if (self.exists == True):
           if (self.hitCount < 7):
               if (GAME_MODE):
                   p.draw.circle(s, WHITE, [self.x, self.y], self.rad, 1)
               angRad = deg2Rad(self.gunAngle)
               self.gunTipX = self.x + self.gunLen*m.cos(angRad)
               self.gunTipY = self.y + self.gunLen*m.sin(angRad)
               if (GAME_MODE):
                   p.draw.line(s, WHITE, [self.x, self.y], [self.gunTipX, self.gunTipY], 1)
           else:
               self.explodeMe(s)
       return
   # drawMe
        
       
   def rotateMe(self, inc):
       self.gunAngle = self.gunAngle + inc
       if (self.gunAngle >= 360):
           self.gunAngle = 0
       elif (self.gunAngle < 0):
           self.gunAngle = 359
       return
   # rotateMe
   
   def moveMe(self, inc):
       self.x = self.x + inc
       if (self.x < self.leftLimit):
           self.x = self.leftLimit
       elif (self.x > self.rightLimit):
           self.x = self.rightLimit
       self.y = self.y
    # moveMe
   
   def getGunTip(self):
       x = self.gunTipX
       y = self.gunTipY
       
       return x, y
   # getGunTip
   
   def getGunAngle(self):
       return self.gunAngle
   # getGunAngle
   
   def explodeMe(self, s):
       if (GAME_MODE):
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad-4, 0)
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad, 0)
           p.draw.circle(s, RED, [int(self.x), int(self.y)], self.rad+4, 0)
           p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.rad+6, 0)
           p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.rad+9, 0)
           p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.rad+11, 0)
           p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.rad+13, 0)
        
       self.exists = False
       return
   # explodeMe

# TURRET
   
# %% FUNCTIONS
def deg2Rad(deg):
    rad = (deg/180.0)*m.pi
    return rad
# deg2Rad

def getDist(x0, y0, x1, y1):
    dist = m.sqrt((x0 - x1)**2 + (y0 - y1)**2)
    return dist
#getDist

def collideTarget(bx, by, bRad, tx, ty, tw, th):
    collision = False
    if ((bx >= tx-tw/2-bRad) and (bx <= (tx+tw/2+bRad))) and ((by >= ty-th/2-bRad) and (by <= (ty+th/2+bRad))):
        collision = True
    return collision
# collideTarget

def collideBomb(bx, by, bRad, Bx, By, Brad):
    collision = False
    myDist = getDist(bx, by, Bx, By)
    if (myDist < (bRad + Brad)):
        collision = True
    return collision
# collideBomb

#closetEnemy
def closestEnemy(listoftargets,turrentx,turrenty):
    distance = 700
    targetdistance = 0
    angle = 0
    for target in listoftargets:
        targetdistance = getDist(turrentx,turrenty,target.x,target.y)
        if(targetdistance < distance):
            distance = targetdistance
            if((turrentx - target.x) == 0):
                angle = 90
            else:
                angle = np.arctan((target.y - turrenty)/(target.x - turrentx))*180/np.pi 
                if angle < 0:
                    angle = angle +180
    return distance/700,angle/180

def closestBomb(listofbombs,turrentx,turrenty):
    distance = 700
    bombdistance = 0
    angle = 0
    for bomb in listofbombs:
        bombdistance = getDist(turrentx,turrenty,bomb.x,bomb.y)
        if(bombdistance < distance):
            distance = bombdistance
            if((turrentx - bomb.x) == 0):
                angle = 90
            else:
                angle = np.arctan((bomb.y - turrenty)/(bomb.x - turrentx))*180/np.pi 
                if angle < 0:
                    angle = angle +180
    return distance/700,angle/180

# %% LEARN GAME FR
def learnGame_ForRealsies(controls):
    
    
    # Count the number of game loops.
    loopcount = 0
    
    # Game stats
    bulletsShot = 0
    bulletHits = 0
    bombsShotDown = 0
    targetsKilled = 0
    
    # Initialize random.
    random.seed()
    
    # Set the width and height of the screen [width, height] .
    size = (screenWidth, screenHeight)
    
    # Set up screen and whatnot.
    screen = None
    if (GAME_MODE):
        p.init()
        screen = p.display.set_mode(size)
        p.display.set_caption("learnGame()")
    
    # Turret postion.
    turrX = (int)(screenWidth/2)
    turrY = screenHeight - 50
    # Create turret
    t = turret(turrX, turrY, 20)
    
    # Create the targets.
    targets = []
    
    if (maxTargets < 1):
        print("Gun Training")
    elif (maxTargets == 1):
        myX = int(screenWidth/2)
        myY = 20
        myTarget = target(myX, myY, 90)
        targets.append(myTarget)
    else:
        for j in range(maxTargets):
            if (j == 0):
                myX = 20
                myY = 20
                targXInc = int((screenWidth - 40)/(maxTargets-1))
                
            else:
                myX = myX + targXInc
                myY = 20
                
            myTarget = target(myX, myY, 90)
            targets.append(myTarget)
    
    # Create bullet array.
    bullets = []
    
    # Create a bomb array.
    bombs = []
    
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
    
    # -------- Main Program Loop -----------
    count = 0
    while running:
        # --- Main event loop
        
        # If playing a game, process keystrokes to control the
        # turret.
        if (GAME_MODE):
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
        
            """ Check for keyboard presses. """
            # key = p.key.get_pressed()
            
            # if (key[p.K_ESCAPE] == True): 
            #     running = False
            
            # Actions that the turret can take.  The
            # user controls this, or a smart controller
            # can control these.
            # if (key[p.K_UP] == True): 
            #     t.moveMe(1)
            # if (key[p.K_DOWN] == True): 
            #     t.moveMe(-1)
            # if (key[p.K_LEFT] == True): 
            #     t.rotateMe(-1)
            # if (key[p.K_RIGHT] == True): 
            #     t.rotateMe(1)
            # if (key[p.K_SPACE] == True):
            #     gx, gy = t.getGunTip()
            #     ang = t.getGunAngle()
            #     bullets.append(bullet(gx, gy, ang))
            #     bulletsShot = bulletsShot + 1
            ang = t.getGunAngle()-180
            closestEnemyDistance, closestEnemyAngle = closestEnemy(turrentx=t.x,turrenty=t.y,listoftargets=targets)
            closestBombDistance, closestBombAngle = closestBomb(turrentx=t.x,turrenty=t.y,listofbombs=bombs)
            # print(ang/180,closestEnemyAngle,closestEnemyDistance,closestBombDistance,closestBombAngle)

            
            output = controls.calcWeightedInput([ang,closestEnemyAngle,closestEnemyDistance,closestBombDistance,closestBombAngle])
            # print(output)
            final = controls.activation(output)
            # print(final)
            if (final[0] == 1): 
                t.moveMe(1)
            if (final[1] == 1): 
                t.moveMe(-1)
            if (final[2] == 1): 
                t.rotateMe(-1)
            if (final[3] == 1): 
                t.rotateMe(1)
            if (final[4] == 1):
                gx, gy = t.getGunTip()
                ang = t.getGunAngle()
                bullets.append(bullet(gx, gy, ang))
                bulletsShot = bulletsShot + 1
            #
        #
                
        # If in simulation mode, turrets actoins are controlled by
        # other means.
        else:
            ang = t.getGunAngle()-180
            closestEnemyDistance, closestEnemyAngle = closestEnemy(turrentx=t.x,turrenty=t.y,listoftargets=targets)
            closestBombDistance, closestBombAngle = closestBomb(turrentx=t.x,turrenty=t.y,listofbombs=bombs)
            #print(ang,closestEnemyAngle,closestEnemyDistance,closestBombDistance,closestBombAngle)

            
            output = controls.calcWeightedInput([ang,closestEnemyAngle,closestEnemyDistance,closestBombDistance,closestBombAngle])
            # print(output)
            final = controls.activation(output)
            #print(final)
            if (final[0] == 1): 
                t.moveMe(1)
            if (final[1] == 1): 
                t.moveMe(-1)
            if (final[2] == 1): 
                t.rotateMe(-1)
            if (final[3] == 1): 
                t.rotateMe(1)
            if (final[4] == 1):
                gx, gy = t.getGunTip()
                ang = t.getGunAngle()
                bullets.append(bullet(gx, gy, ang))
                bulletsShot = bulletsShot + 1
            #
        #
            
        # --- Game logic should go here
        
        # See if a target drops a bomb and see what it selects for a move.
        numTargs = len(targets)
        if (numTargs > 1):
            j = 0
            for targ in targets:
                if (targ.doIExist() == True):
                    # Drop bomb.
                    myChance = random.randint(0, 100)
                    if (myChance < launchBomb):
                        bombBayX, bombBayY = targ.getBombBay()
                        bombs.append(bomb(bombBayX, bombBayY))
                    
                    # Target move.
                    # Find closest target to this target so we do not
                    # run into it.
                    if (j == 0):
                        closeTargX = targets[j+1].x
                    elif (j == (numTargs - 1)):
                        closeTargX = targets[j-1].x
                    else:
                        lDiff = abs(targ.x - targets[j-1].x)
                        rDiff = abs(targ.x - targets[j+1].x)
                        
                        closeTargX = targets[j-1].x
                        if (rDiff < lDiff):
                            closeTargX = targets[j+1].x
                            
                    # Figure out which way to move.
                    myMove = targ.what2Do(closeTargX, targWidth, t.x, 1)
                    # Move.
                    targ.moveMe(myMove)
                    
                    # Update j.
                    j = j+1
                    
        elif (numTargs == 1):
            # Drop bomb.
            myChance = random.randint(0, 100)
            if (myChance < launchBomb):
                bombBayX, bombBayY = targ.getBombBay()
                bombs.append(bomb(bombBayX, bombBayY))
                
            # Move Target based on turret position.
            if (t.x < targets[0].x):
                myMove = left
            elif (t.x > targets[0].x):
                myMove = right
            else:
                myMove = noMove
                
            # Move.
            targets[0].moveMe(myMove)
           
        # --- Move bullets. 
        for b in bullets:
            b.moveMe()
            if (b.doIExist() == False):
                bullets.remove(b)
                # print(len(bullets))
                
        # --- Move bombs.
        for B in bombs:
            B.moveMe()
            if (B.doIExist() == False):
                bombs.remove(B)
        
        # --- Check to see if the bullets hit anything
        
        # Did a bullet hit a bomb?
        for b in bullets:
            for B in bombs:
                if (b.hit == False):
                    if (B.exists == True):
                        b.hit = collideBomb(b.x, b.y, b.radius, B.x, B.y, B.radius)
                        if (b.hit == True):
                            B.hit = True
                            bombsShotDown = bombsShotDown + 1
                 
        # Did a bullet hit a target?
        for b in bullets:
            for targ in targets:
                if (b.hit == False):
                    if (targ.exists == True):
                        b.hit = collideTarget(b.x, b.y, b.radius, targ.x, targ.y, targ.width, targ.height)
                        if (b.hit == True):
                            targ.hitCount = targ.hitCount + 1
                            bulletHits = bulletHits + 1
                          
        # Did a bomb hit the turret?
        for B in bombs:
            if ((B.exists == True) and (B.hit == False)):
                B.hit = collideBomb(B.x, B.y, B.radius, t.x, t.y, t.rad)
                if (B.hit == True):
                    t.hitCount = t.hitCount + 1
                    
        # Remove old targets.
        for targ in targets:
            if (targ.exists == False):
                targets.remove(targ)
                targetsKilled = targetsKilled + 1      
                # print("num targets = ", len(targets))
           
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        if (GAME_MODE) :
            screen.fill(BLACK)

        # --- Drawing code should go here
        # Draw turret.
        t.drawMe(screen)
        
        # Draw bullets.
        for b in bullets:
            b.drawMe(screen)

        # Draw targets.
        for targ in targets:
            targ.drawMe(screen)
            
        # Draw bombs.
        for B in bombs:
            B.drawMe(screen)
                
        # --- Go ahead and update the screen with what we've drawn.
        if (GAME_MODE):
            p.display.flip()
            # Only delay in game mode.
            clock.tick(60)
        
        if ((t.exists == False)or(len(targets) == 0)):
            running = False
            # print("Game Over")
            # Here is where you print the game statistics.
            # print("loopcount: ", loopcount)
            # print("turret was hit this many times: ", turrethitCount)
            # print("bullets shot: ", bulletsShot)
            # print("bullet hits:", bulletHits)
            # print("bombs shot down: ", bombsShotDown)
            # print("targets killed: ", targetsKilled)
            
        loopcount = loopcount + 1

    # Close the window and quit.
    p.quit()
    
    return np.array([loopcount, t.hitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled])
# LEARN GAME

# %% LEARN GAME TRAIN
def learnGameTrain(controls, numberofcontrolls):
    
    
    # Count the number of game loops.
    loopcount = 0
    
    # Game stats
    bulletsShot = 0
    bulletHits = 0
    bombsShotDown = 0
    targetsKilled = 0
    
    # Initialize random.
    random.seed()
    
    # Set the width and height of the screen [width, height] .
    size = (screenWidth, screenHeight)
    
    # Set up screen and whatnot.
    screen = None
    if (GAME_MODE):
        p.init()
        screen = p.display.set_mode(size)
        p.display.set_caption("learnGame()")
    
    # Turret postion.
    turrX = (int)(screenWidth/2)
    turrY = screenHeight - 50
    # Create turret
    t = turret(turrX, turrY, 20)
    
    # Create the targets.
    targets = []
    
    if (maxTargets < 1):
        print("Gun Training")
    elif (maxTargets == 1):
        myX = int(screenWidth/2)
        myY = 20
        myTarget = target(myX, myY, 90)
        targets.append(myTarget)
    else:
        for j in range(maxTargets):
            if (j == 0):
                myX = 20
                myY = 20
                targXInc = int((screenWidth - 40)/(maxTargets-1))
                
            else:
                myX = myX + targXInc
                myY = 20
                
            myTarget = target(myX, myY, 90)
            targets.append(myTarget)
    
    # Create bullet array.
    bullets = []
    
    # Create a bomb array.
    bombs = []
    
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
    
    # -------- Main Program Loop -----------
    count = 0
    while running:
        # --- Main event loop
        
        # If playing a game, process keystrokes to control the
        # turret.
        if (GAME_MODE):
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
        
            """ Check for keyboard presses. """
            # key = p.key.get_pressed()
            
            # if (key[p.K_ESCAPE] == True): 
            #     running = False
            
            # Actions that the turret can take.  The
            # user controls this, or a smart controller
            # can control these.
            # if (key[p.K_UP] == True): 
            #     t.moveMe(1)
            # if (key[p.K_DOWN] == True): 
            #     t.moveMe(-1)
            # if (key[p.K_LEFT] == True): 
            #     t.rotateMe(-1)
            # if (key[p.K_RIGHT] == True): 
            #     t.rotateMe(1)
            # if (key[p.K_SPACE] == True):
            #     gx, gy = t.getGunTip()
            #     ang = t.getGunAngle()
            #     bullets.append(bullet(gx, gy, ang))
            #     bulletsShot = bulletsShot + 1
            
            if (controls[count][0] == 1): 
                t.moveMe(1)
            if (controls[count][1] == 1): 
                t.moveMe(-1)
            if (controls[count][2] == 1): 
                t.rotateMe(-1)
            if (controls[count][3] == 1): 
                t.rotateMe(1)
            if (controls[count][4] == 1):
                gx, gy = t.getGunTip()
                ang = t.getGunAngle()
                bullets.append(bullet(gx, gy, ang))
                bulletsShot = bulletsShot + 1
            #
        #
                
        # If in simulation mode, turrets actoins are controlled by
        # other means.
        else:
            if (controls[count][0] == 1): 
                t.moveMe(1)
            if (controls[count][1] == 1): 
                t.moveMe(-1)
            if (controls[count][2] == 1): 
                t.rotateMe(-1)
            if (controls[count][3] == 1): 
                t.rotateMe(1)
            if (controls[count][4] == 1):
                gx, gy = t.getGunTip()
                ang = t.getGunAngle()
                bullets.append(bullet(gx, gy, ang))
                bulletsShot = bulletsShot + 1
            #
        #
            
        # --- Game logic should go here
        
        # See if a target drops a bomb and see what it selects for a move.
        numTargs = len(targets)
        if (numTargs > 1):
            j = 0
            for targ in targets:
                if (targ.doIExist() == True):
                    # Drop bomb.
                    myChance = random.randint(0, 100)
                    if (myChance < launchBomb):
                        bombBayX, bombBayY = targ.getBombBay()
                        bombs.append(bomb(bombBayX, bombBayY))
                    
                    # Target move.
                    # Find closest target to this target so we do not
                    # run into it.
                    if (j == 0):
                        closeTargX = targets[j+1].x
                    elif (j == (numTargs - 1)):
                        closeTargX = targets[j-1].x
                    else:
                        lDiff = abs(targ.x - targets[j-1].x)
                        rDiff = abs(targ.x - targets[j+1].x)
                        
                        closeTargX = targets[j-1].x
                        if (rDiff < lDiff):
                            closeTargX = targets[j+1].x
                            
                    # Figure out which way to move.
                    myMove = targ.what2Do(closeTargX, targWidth, t.x, 1)
                    # Move.
                    targ.moveMe(myMove)
                    
                    # Update j.
                    j = j+1
                    
        elif (numTargs == 1):
            # Drop bomb.
            myChance = random.randint(0, 100)
            if (myChance < launchBomb):
                bombBayX, bombBayY = targ.getBombBay()
                bombs.append(bomb(bombBayX, bombBayY))
                
            # Move Target based on turret position.
            if (t.x < targets[0].x):
                myMove = left
            elif (t.x > targets[0].x):
                myMove = right
            else:
                myMove = noMove
                
            # Move.
            targets[0].moveMe(myMove)
           
        # --- Move bullets. 
        for b in bullets:
            b.moveMe()
            if (b.doIExist() == False):
                bullets.remove(b)
                # print(len(bullets))
                
        # --- Move bombs.
        for B in bombs:
            B.moveMe()
            if (B.doIExist() == False):
                bombs.remove(B)
        
        # --- Check to see if the bullets hit anything
        
        # Did a bullet hit a bomb?
        for b in bullets:
            for B in bombs:
                if (b.hit == False):
                    if (B.exists == True):
                        b.hit = collideBomb(b.x, b.y, b.radius, B.x, B.y, B.radius)
                        if (b.hit == True):
                            B.hit = True
                            bombsShotDown = bombsShotDown + 1
                 
        # Did a bullet hit a target?
        for b in bullets:
            for targ in targets:
                if (b.hit == False):
                    if (targ.exists == True):
                        b.hit = collideTarget(b.x, b.y, b.radius, targ.x, targ.y, targ.width, targ.height)
                        if (b.hit == True):
                            targ.hitCount = targ.hitCount + 1
                            bulletHits = bulletHits + 1
                          
        # Did a bomb hit the turret?
        for B in bombs:
            if ((B.exists == True) and (B.hit == False)):
                B.hit = collideBomb(B.x, B.y, B.radius, t.x, t.y, t.rad)
                if (B.hit == True):
                    t.hitCount = t.hitCount + 1
                    
        # Remove old targets.
        for targ in targets:
            if (targ.exists == False):
                targets.remove(targ)
                targetsKilled = targetsKilled + 1      
                # print("num targets = ", len(targets))
           
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        if (GAME_MODE) :
            screen.fill(BLACK)

        # --- Drawing code should go here
        # Draw turret.
        t.drawMe(screen)
        
        # Draw bullets.
        for b in bullets:
            b.drawMe(screen)

        # Draw targets.
        for targ in targets:
            targ.drawMe(screen)
            
        # Draw bombs.
        for B in bombs:
            B.drawMe(screen)
                
        # --- Go ahead and update the screen with what we've drawn.
        if (GAME_MODE):
            p.display.flip()
            # Only delay in game mode.
            clock.tick(60)
        
        if ((t.exists == False)or(len(targets) == 0)):
            running = False
            # print("Game Over")
            # Here is where you print the game statistics.
            # print("loopcount: ", loopcount)
            # print("turret was hit this many times: ", turrethitCount)
            # print("bullets shot: ", bulletsShot)
            # print("bullet hits:", bulletHits)
            # print("bombs shot down: ", bombsShotDown)
            # print("targets killed: ", targetsKilled)
            
        loopcount = loopcount + 1
        count = count + 1
        if(count == numberofcontrolls):
            count =  0
    # Close the window and quit.
    p.quit()
    
    return np.array([loopcount, t.hitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled])
# TRAIN

# %% GENETIC ALG
def score(stats):
    # goal >> first 3 stats negative correlation, last 3 stats positive correlation
    fin_score =   (stats[0])*.01 + (stats[1])*25 + (stats[2])*-.01+ (stats[3])*-1 + (stats[4])*-2 +(stats[5])*-5 
    return fin_score
#

def breed(parent1, parent2):
    # first half parent1
    parent1 = parent1[:int(len(parent1)/2)]

    # second half parent2
    parent2 = parent2[int(len(parent2)/2):]

    # parents concatenated
    kid = np.concatenate((parent1, parent2))

    if random.randint(1, 100) < 10:
        kid[random.randint(0, len(kid)-1)] = np.random.randint(2, size = 5)
    #

    return kid
#

def calcWeightedInput(inputs, weights):
    # assumes...
    # len(weights[i]) = len(inputs)

    # multiply weights[i] * inputs = a single WeightedInput 
    WeightedInput = [sum(weight * inputs) for weight in weights]

    return WeightedInput
#

def activation(inputs):

    for indx, input in enumerate(inputs):
        inputs[indx] = 1 / (1 + m.exp(-input))

        if(input < 1):
            inputs[indx] = 0
        else:
            inputs[indx] = 1
        #
    #

    return inputs
#

def geneticAlg(nGen, popSize):
    
    # for each generation in nGen...
    for gen in range(nGen):
        # if first generation...
        if gen == 0:
            # ...create first rndm population >> bool arr, len 5, filled with 0 and 1
            # pop = np.array([[np.random.randint(2, size = 5) for x in range(1000)] for y in range(popSize)])
            # pop = np.array([layer.layer(np.zeros((5), dtype = float), [np.random.random_sample(size = 5) for node in range(0,5)]).weights for individ in range(popSize)])
            pop = [[np.random.random_sample(size = 5) for node in range(0,5)] for individ in range(popSize)]
        #

        # neural net feed
        inputs = np.random.random_sample(size = 5)
        outputs = [calcWeightedInput(inputs, individ) for individ in pop] # weights per perceptron, per individual in pop
        controls = [activation(output) for output in outputs]

        # get stats for each individual in the population
        stats = np.array([learnGameTrain(control, popSize) for control in controls])
        print(stats)
        
    #     # score each individual based on game stats
    #     pop_score = np.array([score(stat) for stat in stats])
    #     #print("\n\n",pop_score)

    #     pop_score_df = pd.DataFrame(pop_score,columns = ['score'])
    #     stats_df = pd.DataFrame(data = stats, columns = ['loopcount','hitten','bullest shot','bullet hits',
    #                                           'bombs shot','targets killed'])
    #     result_df = pop_score_df.join(stats_df).sort_values(by=['score'])
    #     # rank population >> sort()
    #     sort = np.argsort(pop_score) # indx of sorted pop score
    #     # print(stats[sort])
    #     pop = pop[sort] # pop ranked by score sort >> min to max
    #     #print(pop)

    #     # generate new population >>>
    #     # keep certain top percentage of population
    #     top = np.array(pop[:int(len(pop) * 0.3)]) # highest scores from top 20%
    #     # loop through bottom percentage of population...
    #     for individidx in range(int(len(pop)*.3),int(len(pop))):
    #         # choose two parents randomly from top percent
    #         parent1 = top[random.randint(0, len(top)-1)]
    #         parent2 = top[random.randint(0, len(top)-1)]

    #         # produce a kid >> breed(parent1, parent2)
    #         kid = breed(parent1, parent2)

    #         # replace current individual with kid
    #         pop[individidx] = kid
    #     #...fin
    #     print('Gen:',gen)
    #     result_mean = result_df.mean().to_frame().T
    #     display(result_mean)

    # #..fin
    # print(stats_df)
    # display(result_df)
    return # top[0]
#

# %% MAIN
# loopcount, turrethitCount, bulletsShot, bulletHits, bombsShotDown, targetsKilled = learnGame()
# sample_controls = geneticAlg(10, 100)
# print(sample_controls)
# GAME_MODE = True
# print(learnGame(sample_controls,1000))

# inputs = np.random.random_sample(size = 5)
# layer1 = layer.layer([np.random.random_sample(size = 5) for node in range(0,5)])
# output = layer1.calcWeightedInput(inputs)
# final = layer1.activation(output)
# GAME_MODE = True
# print(learnGame(layer1))

# breed weights still use learngame as fitness

geneticAlg(10, 100)