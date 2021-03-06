#Entities.
#Cubes n stuff, yo.

import pygame; from pygame.locals import *
from math import *
from vector_maths import *
from rotations import *
from random import randrange

import resources

#Light class.

class Light():
    def __init__(self, position, luminosity):
        self.position = position
        self.luminosity = luminosity

#Polygon class.

class Polygon():
    def __init__(self, points, colourmod=[0,0,0], texture=None):
        self.points = points
        self.colourmod = colourmod
        counter = 0
        self.average = [0,0,0]
        
        for point in self.points:
            counter += 1
            self.average[0]+=point[0]
            self.average[1]+=point[1]
            self.average[2]+=point[2]
        invcounter = 1/counter
        self.average[0] = self.average[0]*invcounter
        self.average[1] = self.average[1]*invcounter
        self.average[2] = self.average[2]*invcounter

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
        self.average[0] = self.average[0]/counter
        self.average[1] = self.average[1]/counter
        self.average[2] = self.average[2]/counter

#Shape class.

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

#ModelObject class. Used for anything that loads its polygons from a model
#file, rather than being a primitive shape.
class ModelObject():
    
    def __init__(self, size, pos, rotation, model):
        
        self.position = pos
        self.rotation = rotation
        
        self.polygons = model
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

#Ship class. A 3D spaceship.
class Ship(ModelObject):
    
    def __init__(self, size, pos, rotation, spin):
        
        ModelObject.__init__(self, size, pos, rotation, resources.MD_Ship_One)
        self.spin = spin
        
        self.state = "idle"
        self.destination = [0,0,0]
        self.speed = [0,0,0]
        self.acceleration = [0,0,0]
        
        #Ship's turrets
        self.turrets = [Turret(size*0.8,[0,-1.3*size,0],[90,0,0]),
                        Turret(size*0.8,[-2*size,0,0],[90,0,-90])]

    def update(self):
        self.speed = add_3D(self.speed,self.acceleration)
        speed = rotate_3D(self.speed,self.rotation)
        self.rotation = add_3D(self.rotation,self.spin)
        self.position = add_3D(self.position,speed)

        for turret in self.turrets:
            turret.update_relative_to_ship(self.rotation, self.position)
        
class Turret(ModelObject):
    
    def __init__(self, size, pos, rotation):
        
        ModelObject.__init__(self,size,pos,rotation,resources.MD_Turret_One)
        
        #Keeps track of the position and rotation of the parent ship.
        self.shipsrotation = [0,0,0]
        self.shipsposition = [0,0,0]
        
        #Determines whether the turret will track and/or shoot.
        self.state = "active"
        
        #Determines WHAT the turret will track and/or shoot.
        self.target = [0,0,300]
        
        #Point from which projectiles are spawned.
        self.muzzle = [0,120,15]
        
        #Elevation and rotation of the turret.
        self.vert_angle = 0
        self.horz_angle = 0
        
        #Limits for the turret's rotation.
        self.max_elevation = 0
        self.max_rotation = 360
        
        #Degrees per second added to the angle of the turret.
        self.trackingrate = 0.25
        
        self.cooldown = 60
        self.coolcounter = 0
    
    #Turret is in a position and has a rotation relative to that of 
    #it's parent ship, so it needs a new return_polygons function to
    #take account of this.
    def return_polygons(self):
        newpolies = []
        for polygon in self.polygons:
            newpoly = []
            for point in polygon:
                
                #Rotate for elevation/rotation of the turret.
                newpoint = rotate_3D(point,[self.vert_angle,0,self.horz_angle])
                
                #Rotate for the turret's base rotation.
                newpoint = rotate_3D(newpoint,self.rotation)
                
                #Rotate for the ship.
                newpoint = rotate_3D(add_3D(newpoint,self.position),self.shipsrotation)
                
                #Adjust for position of both turret and ship
                newpoint = add_3D(newpoint,self.shipsposition)
                            
                newpoly.append(newpoint)
            newpolies.append(Polygon(newpoly))
        return newpolies
        
    def update(self):
        
        if self.state == "inactive":
            pass
        
        elif self.state == "active":
            #Transform the target until it can be compared with self.muzzle
            target = minus_3D(self.target,self.shipsposition)
            target = rotate_3D(target,minus_3D([0,0,0],self.shipsrotation))
            target = minus_3D(target,self.position)
            target = rotate_3D(target,minus_3D([0,0,0],self.rotation))
            target = rotate_3D(target,minus_3D([0,0,0],[self.vert_angle,0,self.horz_angle]))
            
            diff = minus_3D(target,self.muzzle)
            unit = unit_3D(diff)
            
            if -0.25<unit[0]<0.25 and 0.75<unit[1]<1.25 and -0.25<unit[2]<0.25:
                return self.shoot()
                
            else:
                if unit[0] < 0:
                    self.horz_angle += 0.25
                elif unit[0] > 0:
                    self.horz_angle -= 0.25
                if unit[1] < 0:
                    self.vert_angle += 0.25
                elif unit[1] > 0:
                    self.vert_angle -= 0.25
                    
                if self.vert_angle >= 360:
                    self.vert_angle = 0
                elif self.horz_angle >= 360:
                    self.horz_angle = 0
                    
                if self.vert_angle > self.max_elevation:
                    self.vert_angle = self.max_elevation
                elif self.vert_angle < -self.max_elevation:
                    self.vert_angle = -self.max_elevation
                    
                if self.horz_angle > self.max_rotation:
                    self.horz_angle = self.max_rotation
                elif self.horz_angle < -self.max_rotation:
                    self.horz_angle = -self.max_rotation
        
        elif self.state == "cooldown":
            self.coolcounter+=1
            if self.coolcounter == self.cooldown:
                self.state = "active"
                self.coolcounter = 0
        
        return 0
            
    def shoot(self):
        #Point used to a get a vector from the muzzle.
        point = minus_3D(self.muzzle,[0,-1,0])
        
        #Get the absolute position of the muzzle of the turret.
        muzzle = rotate_3D(self.muzzle,[self.vert_angle,0,self.horz_angle])
        muzzle = rotate_3D(muzzle, self.rotation)
        muzzle = rotate_3D(add_3D(muzzle,self.position),self.shipsrotation)
        muzzle = add_3D(muzzle,self.shipsposition)
        
        #Get the absolute position of the point.
        point = rotate_3D(point,[self.vert_angle,0,self.horz_angle])
        point = rotate_3D(point, self.rotation)
        point = rotate_3D(add_3D(point,self.position),self.shipsrotation)
        point = add_3D(point,self.shipsposition)
        
        #Direction of projectiles
        muzzlevector = minus_3D(point,muzzle)
        muzzleunit = unit_3D(muzzlevector)
        muzzle_velocity = times_scalar_3D(muzzleunit,20)
        
        self.state = "cooldown"
        return [Projectile(muzzle,[0,0,0],muzzle_velocity,100)]
        
    def update_relative_to_ship(self, rotation, pos):
        self.shipsrotation = rotation
        self.shipsposition = pos
    
    def track_target(self, target):
        self.state = "active"
        self.target = target
        
    def stand_down(self):
        self.state - "inactive"
        
class Projectile(Shape):
    def __init__(self,xyz,spin,vel,life):
        n = 3
        polygons =      [[[-n,-n,-n],[ n,-n,-n],[ n, n,-n],[-n, n,-n]],
                         [[ n,-n,-n],[ n,-n, n],[ n, n, n],[ n, n,-n]],
                         [[-n, n,-n],[ n, n,-n],[ n, n, n],[-n, n, n]],
                         [[-n,-n, n],[ n,-n, n],[ n,-n,-n],[-n,-n,-n]],
                         [[ n,-n, n],[-n,-n, n],[-n, n, n],[ n, n, n]],
                         [[-n,-n, n],[-n,-n,-n],[-n, n,-n],[-n, n, n]]]
        
        self.rotation = [0,0,0]
        self.position = xyz
        self.spin = spin
        self.polygons = polygons
        self.velocity = vel
        
        self.state = "live"
        self.duration = life
        
    def update(self):
        self.position = add_3D(self.position,self.velocity)
        self.rotation = add_3D(self.rotation,self.spin)
        self.duration -= 1
        if self.duration == 0:
            self.state = "dead"

# Cube class. A simple 3D cube.

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
                         [[-n,-n, n],[-n,-n,-n],[-n, n,-n],[-n, n, n]]]
        
        self.position = position
        self.rotation = rotation
        self.polygons = polygons

#TextureCube class. A cube that cycles through two textures.

class TextureCube(Cube):
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
    
class ShipSplode():
    def __init__(self, ship):
        self.position = ship.position
        self.lifecounter = 40
        self.l = []
        self.state = "live"
    def update(self):
        self.lifecounter-=1
        if self.lifecounter == 0:
            self.state = "stop"
        for n in range(0,20):
            self.l.append(Projectile(self.position,
                                [randrange(-5,6),
                                 randrange(-5,6),
                                 randrange(-5,6)],
                                [randrange(-5,6),
                                 randrange(-5,6),
                                 randrange(-5,6)],
                                50))
        for n, p in enumerate(self.l):
            p.update()
            if p.state == "dead":
                del self.l[n]
    def return_polygons(self):
        p = []
        for pr in self.l:
            p += pr.return_polygons()
        return p