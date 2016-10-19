import pygame
from pygame.locals import *

from vec3d import vec3d
from vec2d import vec2d

import math

import random

import psyco
psyco.full()

class Emitter():
	
	duration = 20
	spread=math.pi
	particlesPerSecond = 800
	particleSpeed=2
	particleAirResist=0
	particleTypes = []
	
	def __init__(self, pos, vel, acc, origin, groups):
		self.pos=pos
		self.vel=vel
		self.acc=acc
		self.origin=origin
		self.groups = groups
		for group in self.groups:
			group.append(self)
		self.lifetime=0
		self.timesincelastemission=0
		self.particles=[]
	
	def update(self, dt):
		
		self.lifetime += dt
		
		self.pos += self.vel*dt
		self.vel += self.acc*dt
		
		if self.lifetime < self.duration:
			self.emit(dt)
		
		for particle in self.particles:
			particle.update(dt)
	
	def draw(self, surface):
		for particle in self.particles:
			particle.draw(surface)
	
	def emit(self, dt):
		self.timesincelastemission+=dt
		
		alpha = math.atan2(self.vel.x,self.vel.y)
		
		numParticles = int(self.particlesPerSecond/(self.timesincelastemission*100.0))
		for x in range(0,numParticles):
			prt = random.choice(self.particleTypes)
			
			theta = random.random()*self.spread - alpha
			
			v = -vec2d(self.particleSpeed*math.cos(theta),
			          self.particleSpeed*math.sin(theta))
			
			a = -v.normalized()
			a = a*self.particleAirResist
			
			prt(vec2d(0,0),v+self.vel,a,self.origin+self.pos,[self.particles])
			
		if numParticles: self.timesincelastemission=0

class Particle():
	
	startCol=vec3d(255,240,200)
	endCol=vec3d(0,0,0)
	duration=40
	size=8
	
	def __init__(self, pos, vel, acc, origin, groups):
		
		self.col = self.startCol+vec3d(0,0,0)
		self.deltaCol = (self.endCol-self.startCol)/self.duration
		self.pos=pos
		self.vel=vel
		self.acc=acc
		self.origin=origin
		self.rect=Rect(pos,(self.size,self.size))
		self.lifetime=0
		self.groups = groups
		for group in self.groups:
			group.append(self)
	
	def update(self, dt):
		self.pos+=self.vel*dt
		self.vel+=self.acc*dt
		self.col+=self.deltaCol
		if self.col.x < 0: self.col.x = 0
		if self.col.y < 0: self.col.y = 0
		if self.col.z < 0: self.col.z = 0
		self.rect.center = self.pos + self.origin
		self.lifetime+=dt
		if self.lifetime >= self.duration:
			for group in self.groups:
				group.remove(self)
	
	def draw(self, surface):
		pygame.draw.rect(surface, self.col, self.rect)

class EmitterC(Emitter):
	duration = 400
	spread=math.pi*2
	particlesPerSecond = 100
	particleSpeed=2
	particleAirResist=0
	particleTypes = [Particle]
	def __init__(self, pos, vel, acc, origin, groups):
		Emitter.__init__(self, pos, vel, acc, origin, groups)

class EmitterB(Emitter):
	duration = 5
	spread=math.pi*2
	particlesPerSecond = 600
	particleSpeed=5
	particleAirResist=0.2
	particleTypes = [Emitter]
	def __init__(self, pos, vel, acc, origin, groups):
		Emitter.__init__(self, pos, vel, acc, origin, groups)

class ExplosionGenerator():
	
	def __init__(self):
		pygame.init()
		self.clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((800,600))
		self.emitters = []
		Emitter.particleTypes = [Particle]
		
	def getInput(self):
		
		for e in pygame.event.get():
			if e.type == QUIT:
				return 0
			if e.type == MOUSEBUTTONDOWN:
				EmitterB(vec2d(0,0),vec2d(0,0),vec2d(0,0),vec2d(e.pos),[self.emitters])
		return 1
	
	def update(self):
		for emitter in self.emitters:
			emitter.update(1.0)
	
	def draw(self):
		self.screen.fill((0,0,0))
		for emitter in self.emitters:
			emitter.draw(self.screen)
		pygame.display.update()
	
	def mainLoop(self):
		while self.getInput():
			self.update()
			self.draw()
			self.clock.tick(60)
			
expl = ExplosionGenerator()
expl.mainLoop()