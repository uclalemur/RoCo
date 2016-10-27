"""FacePort class.

This module contains the FacePort class.

"""

from SixDOFPort import SixDOFPort

class FacePort(SixDOFPort):
    """A class representing a physical face that can be connected to.

    Attributes:
        face (Face): holds the Face object on the parent graph that this port
        is associated with.

    """
