#==============================================================================
# filters.py
# Mess with images.
#
#==============================================================================

import pygame
from pygame.locals import *

try:
	import Numeric
except:
	Numeric = 0

def apply_function(f, s):
	i = range(0,s.get_width())
	j = range(0,s.get_height())
	if not Numeric:
		if not s.get_locked():
			s.lock()
		for y in j:
			for x in i:
				s.set_at((x,y),f(s.get_at(x,y)))
	else:
		t = pygame.surfarray.array3d(s)
		for x in i:
			for y in j:
				t[x][y] = f(t[x][y])