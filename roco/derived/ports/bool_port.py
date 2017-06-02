"""InBoolPort and OutBoolPort classes.

This module contains the InBoolPort and OutBoolPort classes.

"""

from code_port import CodePort
from base_port import InPort, OutPort

class InBoolPort(InPort, CodePort):
    """A class representing an input port for an integer.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, is_arg=False, **kwargs):
        """Creates an InBoolPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        InPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="bool", **kwargs)
        self.add_allowable_mate(self.__class__)

class OutBoolPort(OutPort, CodePort):
    """A class representing an output port for an integer.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, label, **kwargs):
        """Creates an OutBoolPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            kwargs (dict): additional arguments to override params.
        """
        OutPort.__init__(self, parent, name, **kwargs)
        CodePort.__init__(self, parent, name, label, dtype="bool", **kwargs)
        self.add_allowable_mate(self.__class__)
