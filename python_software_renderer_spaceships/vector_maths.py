#Vector Maths
from math import sqrt, floor
def dot_product_3D(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def cross_product_3D(a,b):
    return[a[1]*b[2] - a[2]*b[1],
           a[2]*b[0] - a[0]*b[2],
           a[0]*b[1] - a[1]*b[0]]
def add_3D(a,b):
    return [a[0]+b[0],
            a[1]+b[1],
            a[2]+b[2]]
def minus_3D(a,b):
    return [a[0]-b[0],
            a[1]-b[1],
            a[2]-b[2]]

def dot_product_2D(a,b):
    return a[0]*b[0] + a[1]*b[1]

def add_2D(a,b):
    return [a[0]+b[0],
            a[1]+b[1]]

def minus_2D(a,b):
    return [a[0]-b[0],
            a[1]-b[1]]

def mag_3D(a):
    return sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])

def unit_3D(a):
    mag = 1/mag_3D(a)
    return [a[0]*mag,
            a[1]*mag,
            a[2]*mag]

def times_scalar_3D(a,b):
    return [a[0]*b,
            a[1]*b,
            a[2]*b]
            
def floor_3D(a):
    return [floor(a[0]),
            floor(a[1]),
            floor(a[2])]
