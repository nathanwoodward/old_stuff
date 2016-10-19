from vec2d import vec2d
import pygame
from pygame.locals import *
import math
import random

class PolygonTrail():
	
	def __init__(self, speed, rotation, thickness, length, randomness,time, get_pos):
		
		self.pos = get_pos()
		self.speed = speed
		self.rotation = rotation
		
		self.left=[]
		self.right=[]
		
		self.length=length
		self.thickness=thickness
		self.randomness=randomness
		
		self.t=time
		self.lastremoval=0
		
		self.get_pos = get_pos
		
	def update(self):
		self.pos = vec2d(self.get_pos())
		
		for point in self.left:
			point[0] += point[1]
			
		for point in self.right:
			point[0] += point[1]
		
		if len(self.left) >= self.length and pygame.time.get_ticks()-self.lastremoval>self.t:
			self.left.remove(self.left[0])
			self.right.remove(self.right[0])
			self.lastremoval = pygame.time.get_ticks()
	
		if len(self.left) <= self.length:
			self.add_points()
	
	def add_points(self):
		
		vel = vec2d(self.speed * math.cos(self.rotation),
					self.speed * math.sin(self.rotation))
		
		dist = (self.thickness+self.thickness*random.random()*self.randomness)/2
		normal = vec2d(vel.y, vel.x).normalized()*dist
		
		leftpoint = self.pos + normal
		rightpoint = self.pos - normal
		
		self.left.append([leftpoint, vel])
		self.right.append([rightpoint, vel])
	
	def draw(self, surface):
		if len(self.left):
			points = []
			for point in self.left:
				points.append(point[0])
			points.append(self.pos)
			for point in reversed(self.right):
				points.append(point[0])
			pygame.draw.polygon(surface,(255,255,255),points)

def main():
	
	pygame.init()
	
	screen = pygame.display.set_mode((800,600))
	
	trail = PolygonTrail(5, 0, 4, 60,0,1, pygame.mouse.get_pos)
	
	clock = pygame.time.Clock()
	
	while 1:
		for e in pygame.event.get():
			if e.type == QUIT:
				pygame.display.quit()
				return
			if e.type == MOUSEMOTION:
				trail.rotation = math.atan2(e.rel[0],-e.rel[1])+math.pi/2
		trail.update()
		screen.fill((0,0,0))
		trail.draw(screen)
		pygame.display.update()
		clock.tick(60)

if __name__ == '__main__':
	main()