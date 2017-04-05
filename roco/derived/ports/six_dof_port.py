"""SixDOFPort class.

This module contains the SixDOFPort class.

"""

from roco.api.port import Port

class SixDOFPort(Port):
    """A class representing a port associated with an object that has 6DOF.
    """
    def __init__(self, parent, obj):
        """Creates a sixdofport object.

        Args:
            parent (component): The component to which this port will be added.
            obj: and object containing six degrees of freedom
        """
        try:
            params = obj.get_6DOF()
        except AttributeError:
            params = get_6DOF(obj)
        Port.__init__(self, parent, params)

    def get_points(self):
        """Gets the points associated with the port

        Args:
            None

        Returns:
            A list with the dx, dy, dz parameters
        """
        return [[self.get_parameter(x) for x in ["dx", "dy", "dz"]]]
