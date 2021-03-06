#=================================================================================================
# thruster.py
# Engines.
#
#=================================================================================================

from maths import Rotate2DVector

class Thruster():
    """ Seemed like a good idea at the time... """
    def __init__(self, object, relative_position, direction, strength):
        """ Object is a reference to whatever's being pushed. """
        self.object = object
        self.position = relative_position
        self.direction = direction
        self.strength = strength
        self.fraction = 0
        self.state = "alive"
    def thrust(self):
        """ Called by self.object, whatever it might be. Uses F=ma"""
        relative_increase = (self.direction[0]*self.strength*self.fraction/self.object.mass, \
                             self.direction[1]*self.strength*self.fraction/self.object.mass)
        absolute_increase = Rotate2DVector(relative_increase,self.object.rotation)
        self.object.accelerate(absolute_increase)