#==============================================================================
# planet.py
# Shwoooooosh PLANETS
#
#==============================================================================

import math, pygame
from pygame.locals import *
import random as Random
from random import random

from maths import *
from noise import MakeNoisyCircle

class Planet():
	""" Class representing a 2D planet. The surface of the planet is represented
		by a circle distored by noise, and mass is approximated from the area of
		the circle (pi*r**2) multiplied by the density of the planet. """
	
	def __init__(self, size, jagginess, density, pos, velocity):
		""" Size: Radius of planet.
			Jagginess: Measure of how noisy the surface looks.
			Density: Density of the material forming the planet. """
			
		self.radius = size + 8
		self.points = MakeNoisyCircle(size,int(size/2),jagginess)
		self.density = density
		self.mass = (2*pi*size*density) * MASSCONVERTER
		self.rotationspeed = (0.1/size)*piby180
		self.pos = pos
		self.velocity = velocity
		self.rotation = 0
		self.thrusters = []
		self.state = "alive"
		
	def draw(self,surf, campos):
		""" Draws the planet to the surface given. The middle of the surface is
			the origin (whim). """
		if not clip_pos_to_screen(self.pos[0], self.pos[1], campos, surf.get_width(), surf.get_height()):
			return
		ncirc = []
		for point in self.points:
			point = Rotate2DVector(point,self.rotation)
			point = ((int(point[0])+surf.get_width()/2+self.pos[0]+campos[0])/campos[2],(int(point[1])+surf.get_height()/2+self.pos[1]+campos[1])/campos[2])
			ncirc.append(point)
			
		pygame.draw.polygon(surf,(100,100,100),ncirc)
		pygame.draw.lines(surf,(255,255,255),1,ncirc,2)

	def F(self, obj):
		""" Returns the strength of the force acting on the objects due to
			their gravitational fields. F1 = F2 = G(m1*m2)/r**2. """
		rsquared = (obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2
		return (G*self.mass*obj.mass)/rsquared

	def fall(self, obj):
		""" Gravitational interaction between two objects. """

		direction = (obj.pos[0]-self.pos[0],obj.pos[1]-self.pos[1])
		inv_magnitude = 1.0/sqrt(direction[0]**2+direction[1]**2)
		direction = (direction[0]*inv_magnitude,direction[1]*inv_magnitude)
		
		# F = (G*m1*m2)/r^2
		# F = ma
		# => a = F/m 
		# => a of self = (G*m2)/r^2
		
		a = (G*obj.mass)/((obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2)
		
		self.accelerate((direction[0]*a,direction[1]*a))

	def accelerate(self, amount):
		""" Accelerate the planet by the vector given. """
		
		self.velocity[0] += amount[0]
		self.velocity[1] += amount[1]

	def move(self):
		""" Moves the planet by its velocity. """
		
		self.pos[0] += self.velocity[0]
		self.pos[1] += self.velocity[1]

	def collide(self, obj, combine=1):
		""" Checks for collisions by comparing the sum of two radii and the
			distance betweem the centres of the two planets.
			"""
		Aradius = self.radius
		Bradius = obj.radius
		dist = sqrt(((obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2))
		if dist < Aradius + Bradius:
			if combine == 1:
				self.combine(obj)
			return 1
		return 0
		
	def combine(self, obj):
		""" Combines two planets. Under construction.
		"""
		
		#=========================================================================================
		# Merge the two sets of points.
		#=========================================================================================
		
		# Get the absolute positions of points, and then test them against the other object,
		# finding a new centre along the way.
		
		for thruster in self.thrusters:
			thruster.state = "dead"
		for thruster in obj.thrusters:
			thruster.state = "dead"
		
		num = 0.0
		position_worldspace = [0,0]
		points_worldspace = []
		
		for point in self.points:
			point = Add2DVector(point,self.pos)
			if Distance1DPoints2D(point,obj.pos) > obj.radius+10:
				points_worldspace.append(point)
				position_worldspace[0]+=point[0]
				position_worldspace[1]+=point[1]
				num += 1
		for point in obj.points:
			point = Add2DVector(point,obj.pos)
			if Distance1DPoints2D(point,self.pos) > self.radius+10:
				points_worldspace.append(point)
				position_worldspace[0]+=point[0]
				position_worldspace[1]+=point[1]
				num += 1
		
		# Work out a new centre - for all the points.
		num = 1.0/num
		position_worldspace[0] = position_worldspace[0]*num
		position_worldspace[1] = position_worldspace[1]*num
		
		points = []
		newradius = 0
		for point in points_worldspace:
			newradius += Distance1DPoints2D(point,position_worldspace)
			points.append(Sub2DVector(point,position_worldspace))
		newradius = newradius * num
		
		# Sort points into clockwise order

		def check(a,b):
			n = b[0]*a[1] - a[0]*b[1]
			return -(n<0) + (n>0)
		points.sort(check)
		
		#=========================================================================================
		# Calculate the physical properties of the new body:
		#=========================================================================================
		
		# Number of points and radius, same as in Planet.
		numpoints = len(points)
		radius = newradius
		
		# Mass is conserved.
		mass = self.mass + obj.mass
		
		# The new density is calculated based on relative size.
		sizeratio = obj.radius/self.radius
		density = (self.density+obj.density*sizeratio)/2.0
		
		# Velocity is calculated using momentum, which is conserved.
		selfmv = [self.mass*self.velocity[0],self.mass*self.velocity[1]]
		objmv = [obj.mass*obj.velocity[0],obj.mass*obj.velocity[1]]
		newmv = Add2DVector(selfmv, objmv)
		
		velocity = [newmv[0]/mass, newmv[1]/mass]
		
		# Position remains the same, but probably shouldn't.
		self.pos = position_worldspace
		
		# Rotation speed is calculated as it is in Planet.
		rotationspeed = 1.0/radius*piby180
		
		# Put it all in place.
		self.radius = newradius
		self.points = points
		self.density = density
		self.mass = mass
		self.rotationspeed = (0.1/radius)*piby180
		self.velocity = velocity
		self.rotation = 0
	
	def update(self):
		""" Updates planet-specific things. """
		
		#self.rotation += self.rotationspeed
		if self.rotation > twopi:
			self.rotation = 0
		elif self.rotation < 0:
			self.rotation = twopi
		self.move()
		
def RandomPlanet(pos, maxsize):
	""" Generate a random bit of rock anwhere within 2000 square...squares of pos. """
	return Planet(Random.randrange(8,maxsize),random()*2,random()*5,[Random.randrange(-8000+pos[0] \
	,8000+pos[0]),Random.randrange(-8000+pos[1],8000+pos[1])],[Random.randrange(-2,3)*random(), \
	Random.randrange(-2,3)*random()])