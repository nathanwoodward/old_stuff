#Functions. Might better be called "Graphics".
#This is the main graphics file.

#Pygame and the maths.
import pygame; from pygame.locals import *
import math; from math import *
from copy import deepcopy, copy
from vector_maths import *

#The rest of the graphics.
from prepare_polygons import *
from rotations import *
from projection import *
from filler import *
from lighting import illuminate
from entities import Polygon, Light

class camera():
    """Are you still there?"""
    def __init__(self, window, pos, angle):
        self.position = pos
        self.angle = angle
        self.field_of_view = [0,0,0]
        self.dist = window[0]/2
        self.size = window
    def move(self,pos):
        """Move the camera"""
        self.position = [self.position[0] + pos[0],self.position[1] + pos[1],self.position[2] + pos[2]]
    def look(self,angle):
        """Change angle"""
        self.angle = [angle[0],angle[1],angle[2]]

def sort(polygons):
    pass
        
def render(renderlist, lights, camera, surface):
    """Draw the polygons to the surface as seen by the camera"""
    
    #Undraw everything, make an empty list.
    surface.fill((100,100,150))
    transformed_polygons = []
    
    # Make camera the origin and rotate everything about it
    # by the camera rotation.
    for polygon in renderlist:
        polygon.colourmod = [0,0,0]
        for light in lights:
            try:illuminate(polygon, light)
            except:pass
        output_points = []
        for point in polygon.points:
            output_points.append(rotate_point_about_camera(point,camera.position,
                                                           camera.angle))
            
        output_polygon = copy(polygon)
        output_polygon.points = output_points
        output_polygon.reaverage()

        if polygon.texture is not None:
            output_P = rotate_point_about_camera(polygon.P,camera.position,
                                                 camera.angle)
            
            output_M = add_3D(polygon.M,polygon.P)
            
            output_M = rotate_point_about_camera(output_M,camera.position,
                                                 camera.angle)
            
            output_M = minus_3D(output_M,output_P)
            
            output_N = add_3D(polygon.N,polygon.P)
            
            output_N = rotate_point_about_camera(output_N,camera.position,
                                                 camera.angle)
            
            output_N = minus_3D(output_N,output_P)

            output_polygon.P = output_P
            output_polygon.M = output_M
            output_polygon.N = output_N
        
        transformed_polygons.append(output_polygon)
        
    #Prepare the polygons for projection.
    renderlist = prepare_polygons_3D(camera,transformed_polygons)
    
    #If they're all gone, there is little point in drawing them...
    if renderlist == None:
        return
    
    #Project the polygons.
    project_polygons(renderlist, camera.size, camera.dist)
    prepare_polygons_2D(camera, renderlist)

    #Outline Everything
    #try:
    #    for poly in renderlist:
    #        pygame.draw.lines(surface,(255,0,0),1,poly.points,10)
    #except:
    #    pass

    #Draw
    try:filler(renderlist, camera, surface)
    except:pass
