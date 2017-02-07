"""EdgePort class.

This module contains the EdgePort class.

"""

from roco.api.port import Port

class EdgePort(Port):
    """A class representing a physical edge that can be connected to.

    Attributes:
        edge (HyperEdge): holds the edge data that the port is associated with.
        edgeName (str): the name of the edge in the parent graph

    """
