import pygame; from pygame.locals import *
import math; from math import *
from lookup import sine, cosine

def rotate(a,angle,b=(0,0)):
    """ Rotate a about b by angle. Make b the origin, then
        rotate a by angle. Then translate by b. """

    #Put the angle in radians, then calculate sine and cosine of it.
    angle = radians(angle)
    sinval = sin(angle)
    cosval = cos(angle)

    #Make about origin.
    rel_A_axis = a[0] - b[0]
    rel_B_axis = a[1] - b[1]

    #Rotate + translate.
    nA = (rel_A_axis * cosval - rel_B_axis * sinval) + b[0]
    nB = (rel_A_axis * sinval + rel_B_axis * cosval) + b[1]

    return (nA,nB)

def rotate_3D(point, angle):
    """ Rotate the point by the angle about the
        origin."""
    if angle == (0,0,0) or angle == [0,0,0]:return point
    #Rotate x and z coordinates about y axis.
    xz = rotate((point[0],point[2]),angle[1])
    #Rotate y and z coordinates about x axis.
    yz = rotate((point[1],xz[1]),angle[0])
    #Rotate x and y coordinates about z axis.
    xy = rotate((xz[0],yz[0]),angle[2])

    return [xy[0],xy[1],yz[1]]

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
    return xyz
