"""The MechanicalComponent class.

This module contains the MechanicalComponent class which is a base class
for all physical objects that have a position and rotation in space.

"""

from roco.api.component import Component
import numpy as np

class MechanicalComponent(Component):
    """A derived component to act as a base for all mechanical objects.

    The MechanicalComponent class adds a layer on top of Component which
    allows it to have dx, dy, dz parameters for location and qa, qi, qj, qk
    quaternion components to represent rotation.

    All mechanical components can also be solved using their constraints and
    relations.
    
    """
    def __init__(self, yaml_file=None, **kwargs):
        Component.__init__(self, yaml_file, **kwargs)
    
    def define(self, origin=False, euler=None, quat=False, **kwargs):
        Component.define(self, **kwargs)
        self.transform3D = np.eye(4)
"""          if origin:
            try:
              x = self.addParameter("dx", 0, dynamic=True)
              y = self.addParameter("dy", 0, dynamic=True)
              z = self.addParameter("dz", 0, dynamic=True)
            except KeyError:
              x = self.getParameter("dx")
              y = self.getParameter("dy")
              z = self.getParameter("dz")
            origin = [x, y, z]
            self.transform3D = np.Matrix(4, 4, lambda i, j: i == j and 1 or j == 3  and origin[i] or 0)
          else:
self.transform3D = np.eye(4)

          if euler:
            try:
              r = self.addParameter("roll", 0, dynamic=True)
              p = self.addParameter("pitch", 0, dynamic=True)
              y = self.addParameter("yaw", 0, dynamic=True)
            except KeyError:
              r = self.getParameter("roll")
              p = self.getParameter("pitch")
              y = self.getParameter("yaw")
            euler = [r, p, y]
            self.transform3D = np.dot(self.transform3D, Yaw(euler[2]))
            self.transform3D = np.dot(self.transform3D, Pitch(euler[1]))
            self.transform3D = np.dot(self.transform3D, Roll(euler[0]))
          elif quat:
            try:
              a = self.addParameter("q_a", 1, dynamic=True)
              b = self.addParameter("q_i", 0, dynamic=True)
              c = self.addParameter("q_j", 0, dynamic=True)
              d = self.addParameter("q_k", 0, dynamic=True)
            except KeyError:
              a = self.getParameter("q_a")
              b = self.getParameter("q_i")
              c = self.getParameter("q_j")
              d = self.getParameter("q_k")
            self.addConstraint(np.Eq(a*a + b*b + c*c + d*d, 1))
            quat = [a, b, c, d]
            self.transform3D = np.dot(self.transform3D, quat2DCM(quat))"""

if __name__ == "__main__":
    pass
    