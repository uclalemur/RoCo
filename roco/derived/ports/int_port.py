"""InIntPort and OutIntPort classes.

This module contains the InIntPort and OutIntPort classes.

"""

from code_port import CodePort
from base_port import InPort, OutPort

class InIntPort(InPort, CodePort):
    """A class representing an input port for an integer.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, is_arg=False, **kwargs):
        """Creates an InIntPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        InPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="int", **kwargs)
        self.add_allowable_mate(self.__class__)

class OutIntPort(OutPort, CodePort):
    """A class representing an output port for an integer.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, **kwargs):
        """Creates an OutIntPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        OutPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="int", **kwargs)
        self.add_allowable_mate(self.__class__)

if __name__ == "__main__":
    pass