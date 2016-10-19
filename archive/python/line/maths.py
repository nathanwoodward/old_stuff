#==============================================================================
# maths.py
# Equals sign, equals sign, equals all the way.
#
#==============================================================================

from math import sin, cos, sqrt, pi, pow,hypot

# Some constants

piby180 = pi/180
twopi = pi*2

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
	
	sinval = sin(angle)
	cosval = cos(angle)
	
	A = vec[0]-origin[0]
	B = vec[1]-origin[1]
	
	return [A*cosval - B*sinval + origin[0], A*sinval + B*cosval + origin[1]]

def Magnitude2DVector(vec):
	return hypot(vec[0],vec[1])

def Unit2DVector(vec):
	m = 1.0/Magnitude2DVector(vec)
	return [m*vec[0],m*vec[1]]

def Distance2DPoints2D(a,b):
	return Sub2DVector(a,b)

def Distance1DPoints2D(a,b):
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

def Project2DTo1D(a, dist, screenxovertwo):
	return int(a[0]*dist/(a[1]+0.00001) + screenxovertwo)