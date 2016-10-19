import math
import pygame
from pygame.locals import *

from vector2D import Vector2D

from line import tileImageAlongLine
from gradient import transparencyGradient

def makePrettyFieldOfView(rect, fov, d, fade):
    
    radius = math.hypot(rect.w/2,rect.h/2)
    
    surf = pygame.Surface((radius*2, radius*2), SRCALPHA)
    
    O = Vector2D(radius, radius)
    
    A = Vector2D(-d, 0)
    B = Vector2D(d, 0)
    C = Vector2D(0, -radius).rotate(fov/2)
    D = Vector2D(0, -radius).rotate(-fov/2)
    
    c = fade
    
    img = transparencyGradient(100,c,(0,0,0,255))
    
    tileImageAlongLine(surf, img, D+O, A+O)
    tileImageAlongLine(surf, img, B+O, C+O)
    
    # Hack: pygame's arc drawing is a bit dodgy.
    offs = 0
    start = start = fov/2+math.pi/2
    end = start + math.pi*2 - fov
    
    for x in range(0, 20):
        
        start += offs
        
        pygame.draw.arc(surf, (0,0,0), surf.get_rect(), start, end,radius)
        
        offs+=0.001
    
    return surf

def main():
    
    class Test():
    
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((800,600))
            self.setFOV(math.pi/3)
            self.setRotation(0)
            
        def setFOV(self, angle):
            self.fov = angle
            self.fovimg = makePrettyFieldOfView(self.screen.get_rect(), self.fov, 0, 20)
        
        def setRotation(self, angle):
            self.rotation = angle
            self.rotatedfovimg = pygame.transform.rotate(self.fovimg, math.degrees(angle))
        
        def rotate(self, angle):
            self.setRotation(self.rotation + angle)
        
        def changefov(self, angle):
            return
            self.setFOV(angle)

        def handleEvents(self):
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    return 1
                
                elif e.type == MOUSEMOTION:
                    if e.rel[0]: self.rotate(math.radians(e.rel[0]))
                
                elif e.type == KEYDOWN:
                    if e.key == K_e:
                        self.setFOV(math.pi/3)
                    elif e.key == K_f:
                        self.setFOV(math.pi - math.pi/9)
                
            return 0
        
        def redraw(self):
            self.screen.fill((50,50,50))
            rect = self.rotatedfovimg.get_rect()
            rect.center = self.screen.get_rect().center
            self.screen.blit(self.rotatedfovimg, rect)
            pygame.display.update()

        def mainLoop(self):
            
            while 1:
                if self.handleEvents():
                    pygame.quit()
                    return
                self.redraw()
    
    Test().mainLoop()
    
if __name__ == '__main__':
    main()