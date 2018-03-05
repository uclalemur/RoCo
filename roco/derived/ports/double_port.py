"""InDoublePort and OutDoublePort classes.

This module contains the InDoublePort and OutDoublePort classes.

"""

from code_port import CodePort
from base_port import InPort, OutPort

class InDoublePort(InPort, CodePort):
    """A class representing an input port for a double.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, is_arg=False, **kwargs):
        """Creates an InDoublePort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        InPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="double", **kwargs)
        self.add_allowable_mate(self.__class__)

class OutDoublePort(OutPort, CodePort):
    """A class representing an output port for a double.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, **kwargs):
        """Creates an OutDoublePort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        OutPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="double", **kwargs)
        self.add_allowable_mate(self.__class__)

if __name__ == "__main__":
    pass