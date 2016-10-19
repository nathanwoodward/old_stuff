#==========================================================================
# pixelaccesstimes.py
# To see what is slow.
# For great justice.
#==========================================================================

#==========================================================================
# Imports
#==========================================================================

import pygame
from pygame.locals import *

import math
from math import sqrt, sin, cos, radians, pi

import random

import numpy

try:
	import psyco
	psyco.full()
except:
	print "Cannot use psyco."

#==========================================================================
# General subroutines.
#==========================================================================

### Insert code here

#==========================================================================
# Classes.
#==========================================================================

### Insert code here

#==========================================================================
# Setup.
#==========================================================================

pygame.init()

res = (320,240)
screen = pygame.display.set_mode((res))
Clock = pygame.time.Clock()
buffer = screen.get_buffer()
print buffer.raw

#==========================================================================
# Subroutines dependent on the above.
#==========================================================================

def One():
	ref = pygame.surfarray.pixels2d(screen)
	xmax = screen.get_width()
	ymax = screen.get_height()
	
	col = (200,200,200)
	
	y = 0
	while y < ymax:
		x = 0
		while x < xmax:
			ref[x][y] = screen.map_rgb(col)
			x += 1
		y += 1

	del ref

def Two():
	pass

def Update():
	#One()
	Two()
	Clock.tick(60)
	print Clock.get_fps()

def Input():
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			return 0
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				return 0
	return 1

#==========================================================================
# Run everything.
#==========================================================================

def main():
	while 1:
		Update()
		if Input() == 0:
			return
		pygame.display.update()

if __name__ == '__main__': main()