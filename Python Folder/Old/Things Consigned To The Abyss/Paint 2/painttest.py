#Paint Program 2

import pygame, os, sys
from pygame.locals import *

class PaintTwoMain:

    def __init__(self, width=800, height=600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width,self.height),
                                              DOUBLEBUF)
        self.screen.fill((0,0,0))
        
    def MainLoop(self, running=1):

        p = PaintInnerWindow()
        self.canvas = p.screen
        self.screen.blit(self.canvas, (p.xpos,p.ypos))
        pygame.display.flip()

        mousepos = pygame.mouse.get_pos()
        oldpos = mousepos
        
        while running == 1:

            mousepressed = pygame.mouse.get_pressed()
            mousepos = pygame.mouse.get_pos()
            mousex = mousepos[0]
            mousey = mousepos[1]
            
            moving = 0
            drawing = 0

            if mousepressed[0] == 1:
                if mousex >= p.xpos:
                    if mousey >= p.ypos:
                        if mousex <= p.xpos + p.width:
                            if mousey <= p.ypos + 20:
                                moving = 1
                            elif mousey <= p.ypos + p.height - 20:
                                drawing = 1
                                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == MOUSEBUTTONUP:
                    drawing = 0
                    moving = 0
                                    
            if moving == 1:
                p.xpos = pygame.mouse.get_pos()[0] - (p.width/2)
                p.ypos = pygame.mouse.get_pos()[1] - 10

            if drawing == 1:
                mousepos = pygame.mouse.get_pos()
                mpos = [(mousepos[0]/2),(mousepos[1]/2)]
                pygame.draw.line(p.screen, (0,0,0), oldpos, mpos)

            p.screen.blit(p.bar,(0,0))
            self.screen.fill((0,0,0))
            self.screen.blit(p.screen,(p.xpos,p.ypos))
            pygame.display.flip()

            oldpos = mpos
                    
        pygame.display.quit()

class PaintInnerWindow:
    
    def __init__(self, width=600, height=400):
        self.width = width
        self.height = height
        self.screen = pygame.Surface((self.width, self.height))
        self.screen.fill((255,255,255))

        self.xpos = 20
        self.ypos = 20

        self.bar = pygame.Surface((self.width, 20))
        self.bar.fill((200,200,200))
        
        self.screen.blit(self.bar, (0,0))

    def update(self):
        return

MainWindow = PaintTwoMain()
MainWindow.MainLoop()