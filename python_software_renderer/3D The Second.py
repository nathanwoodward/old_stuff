#=============================================
#3D The Second
#Better than my last attempt.
#Still pretty damn dodgy.
#=============================================

#=============================================
#Import Libraries
#=============================================
import os, sys
import pygame; from pygame.locals import *

#=============================================
#Import additional files
#=============================================
from functions import *
from get_input import *
from entities import *

from random import choice

#=============================================
#Get external resources
#=============================================
import resources

#=============================================
#SPEEEEEEEEEEEEEEEEEEEEED
#=============================================
try:
    import psyco
    psyco.full()

except: 
    print "Failed to import Psyco"

# This is necessary when passing in tuples to pygame since whereas previously
# it looks like floats were acceptable input, they now aren't.
def itup(ftup):
    return (int(ftup[0]), int(ftup[1]))

#=============================================
#Main Function
#=============================================
def main():

    #=============================================
    #Start pygame.
    #=============================================
    pygame.init()

    #=============================================
    #Size of the display.
    #=============================================
    RES_1 = (1280,800)
    RES_2 = (800,600)
    RES_3 = (640,480)
    RES_4 = (400,300)
    RES_5 = (640,400)
    RES_6 = (320,200)
    RES_7 = (1680,1050)
    
    RES_8 = (300,200)
    
    RES_9 = (100,100)
    RES_10 = (300,300)

    #=============================================
    #Important Constants
    #=============================================
    WINDOWSIZE = RES_6
    SURFACE_ONE = pygame.Surface((WINDOWSIZE))
    ISFULLSCREEN = 0
    TINYWINDOW = 1
    FACTOR = 4.0

    #=============================================
    #Less Important Constants
    #=============================================
    FRAMERATE = 30
    STATS = 1
    FPS = 1
    
    #=============================================
    #Test Scenario To Run
    #=============================================
    SCENARIO = "Ship"

    #=============================================
    #Entities and Lights lists
    #=============================================
    ENTITIES = []
    LIGHTS = []

    if SCENARIO == "Smiley Face":
        #=============================================
        #Smiley Face
        #=============================================

        ENTITIES.append(Cube(50,[-100,0,0],[0,0,0]))
        ENTITIES.append(Cube(50,[-50,0,0],[0,0,0]))
        ENTITIES.append(Cube(50,[0,0,0],[0,0,0]))
        ENTITIES.append(Cube(50,[50,0,0],[0,0,0]))
        ENTITIES.append(Cube(50,[100,0,0],[0,0,0]))

        ENTITIES.append(Cube(50,[-100,-50,0],[0,0,0]))
        ENTITIES.append(Cube(50,[100,-50,0],[0,0,0]))
        ENTITIES.append(Cube(50,[-50,-150,0],[0,0,0]))
        ENTITIES.append(Cube(50,[50,-150,0],[0,0,0]))

        LIGHTS.append(Light([-300,-300,-300],[3,2,1]))

    elif SCENARIO == "Swarm":
        #=============================================
        #Swarm
        #=============================================

        for x in range(0,90):
            ENTITIES.append(RandomCube(300,30))

        LIGHTS.append(Light([0,0,0],[3,2,1]))

    elif SCENARIO == "Particle Soup":
        #=============================================
        #Particle Soup
        #=============================================

        for x in range(0,50):
            ENTITIES.append(RandomCube(9000,30))

        LIGHTS.append(Light([0,0,0],[1,1,1]))

    elif SCENARIO == "Bill":
        #=============================================
        #Bill
        #=============================================

        ENTITIES.append(BillCube(100,
                                 [0,0,0],
                                 [0,0,0],
                                 [1,1,1],
                                 (resources.Bill1_100x100,
                                  resources.Bill1_100x100)
                                 )
                        )

        LIGHTS.append(Light([-300,-300,-300],[10,10,10]))

    elif SCENARIO == "Me":
        #=============================================
        #Me
        #=============================================

        ENTITIES.append(BillCube(100,
                                 [0,0,0],
                                 [0,0,0],
                                 [1,1,1],
                                 (SURFACE_ONE,
                                  resources.Me)
                                 )
                        )

        LIGHTS.append(Light([-300,-300,-300],[1,1,1]))

    elif SCENARIO == "Bill + Swarm":
        #=============================================
        #Bill + Swarm
        #=============================================

        ENTITIES.append(BillCube(100,
                                 [0,0,0],
                                 [0,0,0],
                                 [1,1,1],
                                 (SURFACE_ONE,
                                  SURFACE_ONE)
                                 )
                        )
        
        for x in range(0,30):
            ENTITIES.append(RandomCube(300,30))

        LIGHTS.append(Light([-300,-300,-300],[5,5,5]))

    elif SCENARIO == "Ship":
        #=============================================
        #Ship
        #=============================================
        ENTITIES.append(Ship(40,[-30,50,70],[0,0,0],[1,1,1]))
        LIGHTS.append(Light([-1200,0,0],[5,5,5]))
    
    elif SCENARIO == "city":
        ENTITIES.append(heightmap([-450,400,-450],"output.bmp",90,5))
        LIGHTS.append(OrbitalLight([0,-1000,0],[3,2,1]))
        LIGHTS.append(OrbitalLight([0,1000,0],[1,1,1]))

    #=============================================
    #Set up display
    #=============================================
    if not TINYWINDOW:

        #=============================================
        #Display settings for normal fullscreen
        #=============================================
        if ISFULLSCREEN:
            screen = pygame.display.set_mode(itup(WINDOWSIZE), DOUBLEBUF | HWSURFACE | FULLSCREEN)

        #=============================================
        #Display settings for normal windowed
        #=============================================
        else:
            screen = pygame.display.set_mode(itup(WINDOWSIZE), DOUBLEBUF)
            
    elif TINYWINDOW:

        #=============================================
        #Display settings for blown up fullscreen
        #=============================================
        if ISFULLSCREEN:
            NEWWINDOWSIZE = (WINDOWSIZE[0]*FACTOR,WINDOWSIZE[1]*FACTOR)
            screen = pygame.display.set_mode(itup(NEWWINDOWSIZE), DOUBLEBUF | HWSURFACE | FULLSCREEN)

        #=============================================
        #Display settings for blown up windowed.
        #=============================================
        else:
            NEWWINDOWSIZE = (WINDOWSIZE[0]*FACTOR,WINDOWSIZE[1]*FACTOR)
            screen = pygame.display.set_mode(itup(NEWWINDOWSIZE), DOUBLEBUF)

    #=============================================
    #Set display caption
    #=============================================
    pygame.display.set_caption("3D The Second")

    #=============================================
    #Time
    #=============================================
    CLOCK = pygame.time.Clock()

    #=============================================
    #Changes the camera position depending upon
    #whether or not we're rendering at a tiny
    #resolution.
    #=============================================
    if TINYWINDOW:
        POS = [0,0,-160]
    else:
        POS = [0,0,-1000]
    ANGLE = [0,0,0]

    #=============================================
    #Set up the camera and the display surface
    #=============================================
    CAMERA_ONE = camera(WINDOWSIZE, POS, ANGLE)
    #SURFACE_ONE = pygame.Surface((WINDOWSIZE))

    #=============================================
    #A font.
    #=============================================
    FONT = pygame.font.Font(None, 18)

    #=============================================
    #Main loop.
    #=============================================
    while pygame.display.get_init() == 1:
        
        #=============================================
        #Input
        #=============================================
        for event in pygame.event.get():

            #Exit.
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return
            
            elif event.type == KEYDOWN:
                    
                #Translation
                if event.key == K_w: #Forward
                    MOVING[2] = 1
                if event.key == K_s: #Backward
                    MOVING[2] = -1
                if event.key == K_d: #Right
                    MOVING[0] = 1
                if event.key == K_a: #Left
                    MOVING[0] = -1
                    
            if event.type == KEYUP:
                    
                #Stop Moving.
                if event.key == K_w:
                    MOVING[2] = 0
                if event.key == K_s:
                    MOVING[2] = 0
                if event.key == K_d:
                    MOVING[0] = 0
                if event.key == K_a:
                    MOVING[0] = 0

        if pygame.mouse.get_pressed()[2]:

            A = 50000.0/screen.get_width()
            A = 1.0/A
            
            ROTATE_Y, ROTATE_X = pygame.mouse.get_pos()
            ROTATE_Y -= screen.get_width()/2.0
            ROTATE_X -= screen.get_height()/2.0
            
            CAMERA_ONE.angle[0] += int(-ROTATE_X*A)
            if CAMERA_ONE.angle[0] > 360:
                CAMERA_ONE.angle[0] = 0
            elif CAMERA_ONE.angle[0] < 0:
                CAMERA_ONE.angle[0] = 360
            CAMERA_ONE.angle[1] += int(-ROTATE_Y*A)
            if CAMERA_ONE.angle[1] > 360:
                CAMERA_ONE.angle[1] = 0
            elif CAMERA_ONE.angle[1] < 0:
                CAMERA_ONE.angle[1] = 360

        V = 20

        if MOVING[0] == 1:
            CAMERA_ONE.position[2]+=V*math.sin(math.radians(CAMERA_ONE.angle[1]))
            CAMERA_ONE.position[0]+=V*math.cos(math.radians(CAMERA_ONE.angle[1]))
        elif MOVING[0] == -1:
            CAMERA_ONE.position[2]-=V*math.sin(math.radians(CAMERA_ONE.angle[1]))
            CAMERA_ONE.position[0]-=V*math.cos(math.radians(CAMERA_ONE.angle[1]))
        if MOVING[2] == 1:
            CAMERA_ONE.position[2]+=V*math.cos(math.radians(CAMERA_ONE.angle[1]))*math.cos(math.radians(CAMERA_ONE.angle[0]))
            CAMERA_ONE.position[0]-=V*math.sin(math.radians(CAMERA_ONE.angle[1]))*math.cos(math.radians(CAMERA_ONE.angle[0]))
            CAMERA_ONE.position[1]-=V*math.sin(math.radians(CAMERA_ONE.angle[0]))
        elif MOVING[2] == -1:
            CAMERA_ONE.position[2]-=V*math.cos(math.radians(CAMERA_ONE.angle[1]))*math.cos(math.radians(CAMERA_ONE.angle[0]))
            CAMERA_ONE.position[0]+=V*math.sin(math.radians(CAMERA_ONE.angle[1]))*math.cos(math.radians(CAMERA_ONE.angle[0]))
            CAMERA_ONE.position[1]+=V*math.sin(math.radians(CAMERA_ONE.angle[0]))
            
        CAMERA_ONE.position[0] = floor(CAMERA_ONE.position[0])
        CAMERA_ONE.position[1] = floor(CAMERA_ONE.position[1])
        CAMERA_ONE.position[2] = floor(CAMERA_ONE.position[2])


        #=============================================
        #Update Entities
        #=============================================
        for entity in ENTITIES:
            try:entity.update()
            except:pass
            
        for light in LIGHTS:
            try:light.update()
            except:pass

        #=============================================
        #Update Polygons
        #=============================================
        POLYGONS = []
        
        for ENTITY in ENTITIES:
            for polygon in ENTITY.return_polygons():
                POLYGONS.append(polygon)

        #=============================================
        #Draw everything.
        #=============================================
        render(POLYGONS,LIGHTS,CAMERA_ONE,SURFACE_ONE)

        #=============================================
        #Blitting
        #=============================================
        if not TINYWINDOW:
            screen.blit(SURFACE_ONE, (0,0))
            
        else:
            #=============================================
            #Blow up the surface to fit the screen.
            #=============================================
            screen.blit(pygame.transform.scale(SURFACE_ONE,itup(NEWWINDOWSIZE)),(0,0))
            
        #=============================================
        #Statistics and instructions
        #=============================================
        if FPS:
            screen.blit(FONT.render("FPS: " + str(int(CLOCK.get_fps())),1,(250,250,250)),(5,5))

        if STATS:
            screen.blit(FONT.render("Camera Position: " + str(CAMERA_ONE.position),1,(250,250,250)),(5,30))
            screen.blit(FONT.render("Camera Rotation: " + str(CAMERA_ONE.angle),1,(250,250,250)),(5,55))
            screen.blit(FONT.render("Polygons in scene: " + str(len(POLYGONS)),1,(250,250,250)),(5,80))
            
            screen.blit(FONT.render("WASD: Move the camera along its own X and Z axes.",1,(250,250,250)),(5,105))
            screen.blit(FONT.render("Right Mouse Button: Activates rotation.",1,(250,250,250)),(5,130))

        #=============================================
        #Show
        #=============================================
        pygame.display.flip()

        #=============================================
        #Maintain framerate.
        #=============================================
        CLOCK.tick(FRAMERATE)
        
#=============================================
#Run
#=============================================

if __name__ == "__main__":
    main()

#=============================================
#Profile
#=============================================

#import hotshot
#prof = hotshot.Profile("3D_The_Second")
#prof.runcall(main)
#prof.close()
