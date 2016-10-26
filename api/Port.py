"""Port class.

This module contains the Port class.

"""

from Parameterized import Parameterized

class Port(Parameterized):
    """A class representing an abstract port

    Attributes:
        isInput (bool): whether the port takes input or not.
        isOutput (bool): whether the port gives output or not.
        parent (Component): parent component that this port is tied to.

    """
