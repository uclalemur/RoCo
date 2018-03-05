"""InStringPort and OutStringPort classes.

This module contains the InStringPort and OutStringPort classes.

"""

from roco.derived.ports.code_port import CodePort
from roco.derived.ports.base_port import InPort, OutPort

class InStringPort(InPort, CodePort):
    """A class representing an input port for a string.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, is_arg=False, **kwargs):
        """Creates an InStringPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        InPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="string", **kwargs)
        self.add_allowable_mate(self.__class__)

class OutStringPort(OutPort, CodePort):
    """A class representing an output port for a string.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name,  label, **kwargs):
        """Creates an OutStringPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        OutPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="string", **kwargs)
        self.add_allowable_mate(self.__class__)

if __name__ == "__main__":
    pass
    