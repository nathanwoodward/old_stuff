#=======================================================
#Heightmap Reader
#=======================================================

import pygame
import Numeric
from pygame.locals import *

import loadres

def load_heightmap(pathname, scaleh, scalev):
	#=======================================================
	#Create a 3D representation from a 2D heightmap
	#=======================================================
	
	#=======================================================
	#Load the heightmap
	#=======================================================
	heightmap = loadres.import_bitmap(pathname)
	mapheight = heightmap.get_height()
	mapwidth  = heightmap.get_width()
	
	#=======================================================
	#Create an array to reference the heightmap, and an empty
	#list to store vertices.
	#=======================================================
	heightmap_array = pygame.surfarray.array2d(heightmap)
	coordinate_list = []
	
	#=======================================================
	#Create a list of vertices from the heightmap.
	#=======================================================
	for x, row in enumerate(heightmap_array):
		current_row = []
		for y, pixel in enumerate(row):
			current_row.append([x*scaleh,-heightmap.unmap_rgb(pixel)[0]*scalev,y*scaleh])
		coordinate_list.append(current_row)
			
	#=======================================================
	#Create a list to hold triangles
	#=======================================================
	triangles_list = []
	
	#=======================================================
	# a0---a1---a2---   # <- Each row is two sets of triangles;
	# |\ ta|\ ta|\ ta|  #    each triangle is returned.
	# |tb\ |tb\ |tb\ |  #    
	#  ----b0---b1---b2 #    Number of triangles = 2(width*height)
	#                   #    e.g. 2 * 10 * 21 = 420
	#=======================================================
	y = 0
	
	#=======================================================
	#Loop through points and create triangles from them
	#=======================================================
	while int(y) < mapheight-1:
		x = 0
		while x < mapwidth-1:
			
			#=======================================================
			#Create ta (first) and tb (second).
			#=======================================================
			triangles_list.append([coordinate_list[x][y], coordinate_list[x][y+1], coordinate_list[x+1][y+1] ])
			triangles_list.append([coordinate_list[x+1][y], coordinate_list[x][y], coordinate_list[x+1][y+1] ])
			x += 1
		y += 1
	
	return triangles_list