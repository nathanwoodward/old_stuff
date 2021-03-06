import pygame; from pygame.locals import *
import math; from math import *

def rotate(a,angle,b=(0,0)):

    #Put the angle in radians, then calculate sine and cosine of it.
    angle = radians(angle)
    sinval = sin(angle)
    cosval = cos(angle)

    #Make about origin.
    average_A_axis = a[0] - b[0]
    average_B_axis = a[1] - b[1]

    #Rotate + translate.
    nA = (average_A_axis * cosval - average_B_axis * sinval) + b[0]
    nB = (average_A_axis * sinval + average_B_axis * cosval) + b[1]

    return (nA,nB)

#======================================================
#Rotate 3D
#======================================================
def rotate_3D(point, angle):

    if angle == (0,0,0) or angle == [0,0,0]:return point
    #Rotate x and z coordinates about y axis.
    xz = rotate((point[0],point[2]),angle[1])
    #Rotate y and z coordinates about x axis.
    yz = rotate((point[1],xz[1]),angle[0])
    #Rotate x and y coordinates about z axis.
    xy = rotate((xz[0],yz[0]),angle[2])

    return [xy[0],xy[1],yz[1]]

#def rotate_3D(point, angle):
#    x = point[0]
#    ax = radians(angle[0])
#    y = point[1]
#    ay = radians(angle[1])
#    z = point[2]
#    az = radians(angle[2])
#    
#    #About x
#    
#    xx = x
#    xy = (cos(ax)*y) - (sin(ax)*z)
#    xz = (sin(ax)*y) + (cos(ax)*z)
#    
#    #About y
#    
#    yx = (cos(ay)*xx) + (sin(ay)*xz)
#    yy = xy
#    yz = -(sin(ay)*xx) + (cos(ay)*xz)
#    
#    #About z
#    
#    zx = (cos(az)*yx) - (sin(az)*yy) 
#    zy = (sin(az)*yx) + (cos(az)*yy)
#    zz = yz
#    
#    return [zx,zy,zz]

def rotate_point_about_camera(point, camera_position, camera_angle):
    """Rotates a point about the camera."""
    #point[0]-camera_position[0] makes the camera the origin.
    #Angle is made negative to get it to go in the right direction.
    xyz = rotate_3D(
                    (
                        point[0]-camera_position[0],
                        point[1]-camera_position[1],
                        point[2]-camera_position[2]),
                    (
                        -camera_angle[0],
                        -camera_angle[1],
                        -camera_angle[2])
                    )
    #Projected point transformed so it's on the screen.
    return xyz
