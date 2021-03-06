#Entities.
#Cubes n stuff, yo.

import pygame; from pygame.locals import *
from math import *
from vector_maths import dot_product_3D
from rotations import *
from random import randrange

import resources
try: from heightmap import load_heightmap
except: print "Could not import heightmap."

class Ship():
    
    def __init__(self, size, pos, rotation, spin):

        self.position = pos
        self.rotation = rotation
        self.spin = spin
        
        self.polygons = resources.MD_Ship_Two
        faces = []
        for points in self.polygons:
            newpoints = []
            for point in points:
                newpoints.append([point[0]*size,
                                  point[1]*size,
                                  point[2]*size])
            faces.append(newpoints)
        self.polygons = faces
                    
    def return_polygons(self):
        newpolies = []
        for polygon in self.polygons:
            newpoly = []
            for point in polygon:
                newpoint = rotate_3D(point,self.rotation)
                newpoint = [newpoint[0]+self.position[0],
                            newpoint[1]+self.position[1],
                            newpoint[2]+self.position[2]]
                newpoly.append(newpoint)
            newpolies.append(Polygon(newpoly))
        return newpolies

    def update(self):
        self.rotation[0] += self.spin[0]
        self.rotation[1] += self.spin[1]
        self.rotation[2] += self.spin[2]

def RandomCube(posmax, sizemax):
    return LolCube(randrange(10,sizemax),
                   [randrange(-posmax,posmax),randrange(-posmax,posmax),randrange(-posmax,posmax)],
                   [randrange(0,360),randrange(0,360),randrange(0,360)],
                   [randrange(-1,2),randrange(-1,2),randrange(-1,2)]
                   )

class Light():
    def __init__(self, position, luminosity):
        self.position = position
        self.luminosity = luminosity
        
class OrbitalLight():
    def __init__(self,position, luminosity):
        self.position = position
        self.luminosity = luminosity
        self.spin = [2,0,0]
    def update(self):
        self.position = rotate_3D(self.position,self.spin)

class Polygon():
    def __init__(self, points, colour=[100,100,100], texture=None):
        self.points = points
        self.colour = colour
        self.colourmod = [0,0,0]
        counter = 0
        self.average = [0,0,0]
        self.shown = "yes"
        
        for point in self.points:
            counter += 1
            self.average[0]+=point[0]
            self.average[1]+=point[1]
            self.average[2]+=point[2]
        invcounter = 1.0/counter
        self.average[0] = self.average[0]*invcounter
        self.average[1] = self.average[1]*invcounter
        self.average[2] = self.average[2]*invcounter
        
        self.az = self.average[2]

        self.texture = texture
        if self.texture is not None:
            self.P = self.points[0]
            self.M = [self.points[1][0] - self.points[0][0],
                      self.points[1][1] - self.points[0][1],
                      self.points[1][2] - self.points[0][2]]
            self.N = [self.points[3][0] - self.points[0][0],
                      self.points[3][1] - self.points[0][1],
                      self.points[3][2] - self.points[0][2]]

    def reaverage(self):
        self.average = [0,0,0]
        counter = 0
        for point in self.points:
            counter += 1
            self.average[0]+=point[0]
            self.average[1]+=point[1]
            self.average[2]+=point[2]
        invcounter = 1.0/counter
        self.average[0] = self.average[0]*invcounter
        self.average[1] = self.average[1]*invcounter
        self.average[2] = self.average[2]*invcounter
        
        self.az = self.average[2]
        
    def __cmp__(self,other):
        return cmp(self.average[2],other.average[2])
        
class Shape():
    def return_polygons(self):
        newpolies = []
        for polygon in self.polygons:
            newpoly = []
            for point in polygon:
                newpoint = rotate_3D(point,self.rotation)
                newpoint = [newpoint[0]+self.position[0],
                            newpoint[1]+self.position[1],
                            newpoint[2]+self.position[2]]
                newpoly.append(newpoint)
            newpolies.append(Polygon(newpoly))
        return newpolies
    
class heightmap(Shape):
    def __init__(self,pos, img, hscale,vscale):
        self.polygons = load_heightmap(img,hscale,vscale)
        self.position = pos
        self.rotation = [0,0,0]
    def update(self):
        pass

class Cube(Shape):
    def __init__(self, size, position, rotation, texture=None):
        if texture is not None:
            self.istexture = 1
        else: self.istexture = 0
        self.texture = texture
        n = size/2.0
        polygons =      [[[-n,-n,-n],[ n,-n,-n],[ n, n,-n],[-n, n,-n]],
                         [[ n,-n,-n],[ n,-n, n],[ n, n, n],[ n, n,-n]],
                         [[-n, n,-n],[ n, n,-n],[ n, n, n],[-n, n, n]],
                         [[-n,-n, n],[ n,-n, n],[ n,-n,-n],[-n,-n,-n]],
                         [[ n,-n, n],[-n,-n, n],[-n, n, n],[ n, n, n]],
                         [[-n,-n, n],[-n,-n,-n],[-n, n,-n],[-n, n, n]]
                        ]
        self.position = position
        self.rotation = rotation
        self.polygons = polygons

class LolCube(Cube):
    def __init__(self, size, position, rotation, spin):
        Cube.__init__(self, size, position, rotation)
        self.spin = spin
    def update(self):
        newpolies = []
        self.position = rotate_3D(self.position,self.spin)
        self.rotation[0] += self.spin[0]
        self.rotation[1] += self.spin[1]
        self.rotation[2] += self.spin[2]
    def return_polygons(self):
        newpolies = []
        for polygon in self.polygons:
            newpoly = []
            for point in polygon:
                newpoint = rotate_3D(point,self.rotation)
                newpoint = [newpoint[0]+self.position[0],
                            newpoint[1]+self.position[1],
                            newpoint[2]+self.position[2]]
                newpoly.append(newpoint)
            if self.istexture ==1:
                newpolies.append(Polygon(newpoly,[0,0,0],self.texture,[newpoly[0],newpoly[1],newpoly[3]]))
            elif self.istexture ==0:
                newpolies.append(Polygon(newpoly))
                
        return newpolies

class BillCube(Cube):
    def __init__(self, size, position, rotation, spin, textures):
        Cube.__init__(self, size, position, rotation, textures[0])
        self.spin = spin
        self.textures = textures
        self.texturepointer = 0
        self.counter = 0
    def update(self):
        self.rotation[0] += self.spin[0]
        self.rotation[1] += self.spin[1]
        self.rotation[2] += self.spin[2]
        if self.counter < 60:
            self.texturepointer = 0
        elif self.counter > 60:
            self.texturepointer = 1

        if self.counter > 120:
            self.counter = 0

        self.counter += 1
    def return_polygons(self):
        newpolies = []
        for polygon in self.polygons:
            newpoly = []
            for point in polygon:
                newpoint = rotate_3D(point,self.rotation)
                newpoint = [newpoint[0]+self.position[0],
                            newpoint[1]+self.position[1],
                            newpoint[2]+self.position[2]]
                newpoly.append(newpoint)
            newpolies.append(Polygon(newpoly,[0,0,0],self.textures[self.texturepointer]))
        return newpolies
