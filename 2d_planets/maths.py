#==============================================================================
# maths.py
# Equals sign, equals sign, equals all the way.
#
#==============================================================================

from math import sin, cos, sqrt, pi, pow

# Some constants

piby180 = pi/180
twopi = pi*2

# Some physical constants

G =0.667 # G is borked, as scale is borked.
MASSCONVERTER = 1
c = 3*pow(10,16)
csquared = 9*pow(10,16)

#======================================================================
# 2D Vector maths
#======================================================================

def Add2DVector(a,b):
	return [a[0]+b[0],a[1]+b[1]]

def Sub2DVector(a,b):
	return [a[0]-b[0],a[1]-b[1]]

def Mul2DVector(a,b):
	return [a[0]*b[0],a[1]*b[1]]

def ScalMul2DVector(a,n):
	return [a[0]*n,a[1]*n]

def DotProduct2DVector(a, b):
	return a[0]*b[0] + a[1]*b[1]
def Rotate2DVector(vec, angle, origin=[0,0]):
	""" Rotate a 2D vector of the form [x,y] by angle (in radians) about origin,
		which defaults to [0,0]. """
	
	sinval = sin(angle)
	cosval = cos(angle)
	
	A = vec[0]-origin[0]
	B = vec[1]-origin[1]
	
	return [A*cosval - B*sinval + origin[0], A*sinval + B*cosval + origin[1]]

def Magnitude2DVector(vec):
	""" Get the magnitude of a 2D vector of the form [x,y]. """
	return sqrt(vec[0]**2+vec[1]**2)

def Unit2DVector(vec):
	""" Get the direction of a 2D vector. """
	m = 1.0/Magnitude2DVector(vec)
	return [m*vec[0],m*vec[1]]

def Distance2DPoints2D(a,b):
	""" Get the distance between two 2D vectors of the form [x,y], in the form
		[x,y]. Well, ok, displacement. """
	return Sub2DVector(a,b)

def Distance1DPoints2D(a,b):
	""" Get the distance between two 2D vectors of the form [x,y], in the form
		D. """
	return Magnitude2DVector(Sub2DVector(a,b))

#======================================================================
# 3D Vector Maths
#======================================================================

def Add3DVector(a,b):
	return [ a[0]+b[0], a[1]+b[1], a[2]+b[2] ]

def Sub3DVector(a,b):
	return [ a[0]-b[0], a[1]-b[1], a[2]-b[2] ]

def CrossProduct3DVector(a,b):
	return [ a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0] ]

def DotProduct3DVector(a,b):
	return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def Mul3DVector(a,x):
	return [a[0]*x, a[1]*x, a[2]*x]

def Rotate3DVector(a, angles, origin=[0,0,0]):
	a = Sub3DVector(a, origin)
	Y, Z = Rotate2DVector([a[1], a[2]], angles[0])
	X, Z = Rotate2DVector([a[0],  Z  ], angles[1])
	X, Y = Rotate2DVector([ X   , Y  ], angles[2])
	return Add3DVector([X,Y,Z], origin)

def Magnitude3DVector(a):
	return sqrt(a[0]**2+a[1]**2+a[2]**2)

def Unit3DVector(a):
	m = 1.0/Magnitude3DVector(a)
	return [a[0]*m,a[1]*m,a[2]*m]

def Distance3D_1D(a,b):
	return Magnitude3DVector(Sub3DVector(a,b))

#======================================================================

def Project3DTo2D(a, surface, dist, screenx=0, screeny=0):
	c = dist/(a[2]+0.00001)
	return a[0]*c+screenx, a[1]*c+screeny

#======================================================================

def world_to_screen(x, y, campos, screenx, screeny):
	X = int((x + screenx*0.5 + campos[0]) / (campos[2] + 0.000001))
	Y = int((y + screeny*0.5 + campos[1]) / (campos[2] + 0.000001))
	return X, Y

def screen_to_world(X, Y, campos, screenx, screeny):
	x = X * campos[2] - (campos[0] + screenx * 0.5)
	y = Y * campos[2] - (campos[1] + screeny * 0.5)
	return x, y

def clip_pos_to_screen(x, y, campos, screenx, screeny):
	X, Y = world_to_screen(x, y, campos, screenx, screeny)
	if 0 < X < screenx and 0 < Y < screeny:
		return 1
	return 0