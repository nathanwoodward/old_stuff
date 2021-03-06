#====================================================
#filler.py
#Scan conversion, polygon filling and clipping to
#the screen.
#====================================================

#====================================================
#Filling is slow, seeing as how it takes for ever to 
#get pixels from place to place. It all works, though.
#
#Depth sort thing needs replacing.
#====================================================

#====================================================
#Import modules
#====================================================
import pygame; from pygame.locals import *
from math import *

#====================================================
#Import additional modules
#====================================================
from vector_maths import *

#====================================================
#Constants
#====================================================
global inv_255
inv_255 = 1/255.0

def get_edges(polygon):
    #====================================================
    #Turns a list of points into a list of edges.
    #====================================================
    counter = 0
    edges = []
    while counter < len(polygon.points):
        edges.append([polygon.points[counter],polygon.points[counter-1]])
        counter += 1
    return edges

def side(edge):
    #====================================================
    #Checks for leftness or rightness. Left = 1
    #====================================================
    if edge[0][1] > edge[1][1]:
        return 0
    else:
        return 1

def horz(edge):
    #====================================================
    #Checks for horizontalness. Returns 1 if this is so.
    #====================================================
    if edge[0][1] == edge[1][1]:
        return 1
    else: return 0

def sort(polygons):
    #====================================================
    #Depth sort. Needs replacing with something good.
    #====================================================
    return polygons.sort(reverse=1)

def clip(polygon, camera_size):
    right = camera_size[0]
    bottom = camera_size[1]
    
    #====================================================
    #Fail = 1 ==> Polygon is culled
    #====================================================
    fail = 0
    print "NONE" , polygon.points
    #====================================================
    #Clip Left
    #====================================================
    current = 1
    previous = 0
    newpoints = []
    
    while current < len(polygon.points):
        
        #====================================================
        #Current out, previous out
        #====================================================
        if polygon.points[current][0] > 0 and polygon.points[previous][0] > 0:
            pass
        
        #====================================================
        #Current out, previous in
        #====================================================
        elif polygon.points[current][0] < 0 and polygon.points[previous][0] > 0:
            m = (polygon.points[current][1]-polygon.points[previous][1])/(polygon.points[current][0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            y = 0 + c
            newpoints.append([0,y])
            
        #====================================================
        #Current in, previous in
        #====================================================            
        elif polygon.points[current][0] > 0 and polygon.points[previous][0] > 0:
            newpoints.append(polygon.points[current])
            
        #====================================================
        #Current in, previous out
        #====================================================            
        elif polygon.points[current] > 0 and polygon.points[previous][0] < 0:
            m = (polygon.points[current][1]-polygon.points[previous][1])/(polygon.points[current][0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            y = 0 + c
            newpoints.append([0,y])
            newpoints.append(current)
            
        current += 1
        previous += 1
    
    polygon.points = newpoints
    
    print "LEFT" , polygon.points
    #====================================================
    #Clip Right
    #====================================================
    current = 1
    previous = 0
    newpoints = []
    
    while current < len(polygon.points):
        
        #====================================================
        #Current out, previous out
        #====================================================
        print polygon.points
        if polygon.points[current][0] > right and polygon.points[previous][0] > right:
            pass
        
        #====================================================
        #Current out, previous in
        #====================================================
        elif polygon.points[current][0] > right and polygon.points[previous][0] < right:
            m = (polygon.points[current]-polygon.points[previous][1])/(polygon.points[current]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            y = right*m + c
            newpoints.append([right,y])
            
        #====================================================
        #Current in, previous in
        #====================================================            
        elif polygon.points[current][0] < right and polygon.points[previous][0] < right:
            newpoints.append(polygon.points[current])
            
        #====================================================
        #Current in, previous out
        #====================================================            
        elif polygon.points[current] < right and polygon.points[previous][0] > right:
            m = (polygon.points[current][1]-polygon.points[previous][1])/(polygon.points[current][0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            y = right*m + c
            newpoints.append([right,y])
            newpoints.append(polygon.points[current])
            
        current += 1
        previous += 1
    
    polygon.points = newpoints
    
    print "RIGHT" , polygon.points
    #====================================================
    #Clip Top
    #====================================================
    current = 1
    previous = 0
    newpoints = []
    
    while current < len(polygon.points):
        
        #====================================================
        #Current out, previous out
        #====================================================
        if polygon.points[current][1] < 0 and polygon.points[previous][1] < 0:
            pass
        
        #====================================================
        #Current out, previous in
        #====================================================
        elif polygon.points[current][1] < 0 and polygon.points[previous][1] > 0:
            m = (current[1]-polygon.points[previous][1])/(current[0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            x = (0 - c)/m
            newpoints.append([x,0])
            
        #====================================================
        #Current in, previous in
        #====================================================            
        elif polygon.points[current][1] > 0 and polygon.points[previous][1] > 0:
            newpoints.append(polygon.points[current])
            
        #====================================================
        #Current in, previous out
        #====================================================            
        elif polygon.points[current][1] > 0 and polygon.points[previous][1] < 0:
            m = (current[1]-polygon.points[previous][1])/(current[0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            x = (0 - c)/m
            newpoints.append([x,0])
            newpoints.append(polygon.points[current])
            
        current += 1
        previous += 1
    
    polygon.points = newpoints
    
    print "TOP" , polygon.points
    #====================================================
    #Clip Bottom
    #====================================================
    current = 1
    previous = 0
    newpoints = []
    
    while current < len(polygon.points):
        
        #====================================================
        #Current out, previous out
        #====================================================
        if polygon.points[current][1] > bottom and polygon.points[previous][1] > bottom:
            pass
        
        #====================================================
        #Current out, previous in
        #====================================================
        elif polygon.points[current][1] > bottom and polygon.points[previous][1] < bottom:
            m = (current[1]-polygon.points[previous][1])/(current[0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            x = (bottom - c)/m
            newpoints.append([x,bottom])
            
        #====================================================
        #Current in, previous in
        #====================================================            
        elif polygon.points[current][1] < bottom and polygon.points[previous][1] < bottom:
            newpoints.append(polygon.points[current])
            
        #====================================================
        #Current in, previous out
        #====================================================            
        elif polygon.points[current][1] < bottom and polygon.points[previous][1] > bottom:
            m = (polygon.points[current][1]-polygon.points[previous][1])/(polygon.points[current][0]-polygon.points[previous][0])
            c = polygon.points[previous][1]-(m*polygon.points[previous][0])
            x = (bottom - c)/m
            newpoints.append([x,bottom])
            newpoints.append(polygon.points[current])
            
        current += 1
        previous += 1
    
    polygon.points = newpoints
    print "BOTTOM" , polygon.points

def get_limits(edges, camera_size):
    #====================================================
    #Gets scanlines.
    #====================================================
    
    #====================================================
    #Lists of start and end x values.
    #====================================================
    left = limits_array(camera_size)
    right = limits_array(camera_size)
    
    #====================================================
    #Max and min y.
    #====================================================
    minmax = [edges[0][0][1],edges[0][0][1]]
    
    for edge in edges:
        #====================================================
        #Get min and max y values for this polygon.
        #====================================================
        if edge[0][1] < minmax[0]:
            minmax[0] = edge[0][1]
        elif edge[0][1] > minmax[1]:
            minmax[1] = edge[0][1]
        if edge[1][1] < minmax[0]:
            minmax[0] = edge[1][1]
        elif edge[1][1] > minmax[1]:
            minmax[1] = edge[1][1]

        #====================================================
        #Horizontal edges are ignored - they are not needed for scanlines.
        #====================================================
        if horz(edge) != 1:
            
            #====================================================
            #A left edge. First point is higher than the last.
            #====================================================
            if side(edge) == 1:
                
                #====================================================
                #Gradient of the edge (change in x for a change in y)
                #====================================================
                change_in_x_per_y = (edge[1][0] - edge[0][0]) / \
                                    (edge[1][1] - edge[0][1])

                #====================================================
                #First and last values of y.
                #====================================================
                start_y = int(ceil(edge[0][1]))
                end_y = int(ceil(edge[1][1]))

                #====================================================
                #Initial value of x.
                #====================================================
                x = edge[0][0] + (float(start_y) - edge[0][1]) * change_in_x_per_y

                #====================================================
                #Loop through rows and mark left and right x limits.
                #====================================================
                y = start_y
                while y < end_y:
                    left[y] = ceil(x)
                    x += change_in_x_per_y 
                    y += 1
            
            #====================================================
            #A right edge. First point is lower than the last.
            #====================================================
            else:
                
                #====================================================
                #Gradient is opposite for a right edge.
                #====================================================
                change_in_x_per_y = (edge[0][0] - edge[1][0]) / \
                                    (edge[0][1] - edge[1][1])
                
                #====================================================
                #First and last values of y.
                #====================================================
                start_y = int(ceil(edge[1][1]))
                end_y = int(ceil(edge[0][1]))
                
                #====================================================
                #Initial value of x.
                #====================================================
                x = edge[1][0] + (float(start_y) - edge[1][1]) * change_in_x_per_y

                #====================================================
                #Loop through rows and mark left and right x limits.
                #====================================================
                y = start_y
                while y < end_y:
                    right[y] = ceil(x)
                    x += change_in_x_per_y 
                    y += 1
                    
    #====================================================
    #Returns 1.) left limits for scanlines, 2) right limits
    #for scanlines and 3) min and max y values of the polygon.
    #====================================================
    return left, right, minmax

def limits_array(camera_size):
    #====================================================
    #Returns a blank list as high as the camera.
    #====================================================
    lim = []
    for y in range(0,camera_size[1]+1):
        lim.append(0)
    return lim

#====================================================
#Code has been stolen to speed the damn thing up.
#====================================================
def sort_by_attr2(seq,attr):
    import operator
    intermed = [ (getattr(seq[i],attr), i, seq[i]) for i in xrange(len(seq)) ]
    intermed.sort(reverse=1)
    return [ tup[-1] for tup in intermed ]
#====================================================
#/Theft.
#====================================================
    
def filler(polygons, camera, surface):
    camera_size = camera.size

    polygons = sort_by_attr2(polygons,"az")
    surface.lock()
    
    for polygon in polygons:
        #clip(polygon,camera_size)
        if len(polygon.points) < 3:
            polygon.shown = "no"
        if polygon.shown == "yes":
            
            #====================================================
            #Faaaaaaaast - for untextured polygons
            #====================================================
            if polygon.texture is None:

                colour = [100,100,100]
                colour[0] = int(colour[0]*polygon.colourmod[0]*inv_255)
                colour[1] = int(colour[1]*polygon.colourmod[1]*inv_255)
                colour[2] = int(colour[2]*polygon.colourmod[2]*inv_255)
                
                if colour[0] > 255: colour[0] = 255
                if colour[1] > 255: colour[1] = 255
                if colour[2] > 255: colour[2] = 255
                
                colour = surface.map_rgb(colour)

                pygame.draw.polygon(surface,colour,polygon.points)

            #====================================================
            #Sloooooooow - for textured polygons
            #====================================================
            elif polygon.texture is not None:

                edges = get_edges(polygon)
                
                left, right, minmax = get_limits(edges, camera_size)

                P = polygon.P
                M = polygon.M
                N = polygon.N

                A = cross_product_3D(P,N); Ax = A[0]; Ay = A[1]; Az = A[2];
                B = cross_product_3D(M,P); Bx = B[0]; By = B[1]; Bz = B[2];
                C = cross_product_3D(N,M); Cx = C[0]; Cy = C[1]; Cz = C[2];

                xmod = camera.size[0]/2
                ymod = camera.size[1]/2

                S = [0,0,camera.dist]

                surf = pygame.surfarray.pixels2d(surface)
                tex = pygame.surfarray.array2d(polygon.texture.convert_alpha())

                for y in range(minmax[0]+1, minmax[1]+1):

                    S[1] = y - ymod

                    leftlim = int(left[y])
                    rightlim = int(right[y])

                    if leftlim < rightlim:

                        row = surf[leftlim:rightlim,y]

                        S[0] = leftlim - xmod
                        
                        screenx = S[0]
                        screeny = S[1]
                        DIST = S[2]

                        a = (screenx * Ax) + (screeny * Ay) + (DIST * Az) - Ax
                        b = (screenx * Bx) + (screeny * By) + (DIST * Bz) - Bx
                        c = (screenx * Cx) + (screeny * Cy) + (DIST * Cz) - Cx
                        
                        for x in range(leftlim,rightlim):

                            a += Ax
                            b += Bx
                            c += Cx
                            
                            invc = 1.0/c
                            u = int((polygon.texture.get_width()-1) * a * invc)
                            v = int((polygon.texture.get_height()-1) * b * invc)
                            
                            col = surface.unmap_rgb(tex[u][v])
                            col = [int(col[0]*polygon.colourmod[0]*inv_255),
                                   int(col[1]*polygon.colourmod[1]*inv_255),
                                   int(col[2]*polygon.colourmod[2]*inv_255)]

                            if col[0] > 255: col[0] = 255
                            if col[1] > 255: col[1] = 255
                            if col[2] > 255: col[2] = 255
                            
                            row[x-leftlim] = surface.map_rgb(col)

                        surf[leftlim:rightlim,y] = row
    surface.unlock()
