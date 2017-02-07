"""The MechanicalComponent class.

This module contains the MechanicalComponent class which is a base class
for all physical objects that have a position and rotation in space.

"""

from roco.api.Component import Component

class MechanicalComponent(Component):
    """A derived component to act as a base for all mechanical objects.

    The MechanicalComponent class adds a layer on top of Component which
    allows it to have dx, dy, dz parameters for location and qa, qi, qj, qk
    quaternion components to represent rotation.

    All mechanical components can also be solved using their constraints and
    relations.
    
    """
