"""CodePort class.

This module contains the CodePort class as well as the following classes that derive from it:
OutPort, InPort, InStringPort, OutStringPort, InIntPort, OutIntPort, InFloatPort, OutFloatPort, InDoublePort, OutDoublePort.

"""

from roco.api.port import Port

class CodePort(Port):
    """A class representing a code port



    """

    def __init__(self, parent, name, label, dtype=None, **kwargs):
        """Creates a CodePort Object

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            label (str): label of the port.
            dtype (str): datatype of the code snippet
            kwargs (dict): additional arguments to override params.

        """
        Port.__init__(self, parent, {}, **kwargs)
        self.add_parameter("label", label, is_symbol=False)
        self.type = dtype
        self.set_name(name)
        self.label = label

    def can_mate(self, other_port):
        """Returns true if this port can mate with other_port and false otherwise.
        Overrides inherited implementation

        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are compatible.
        """
        if self.type is None or other_port.type is None:
            return True
        return self.type == other_port.type

    def constrain(self, parent, to_port,  **kwargs):
        """Return a set of semantic constraints to be satisfied when connecting to to_port object.
        Overrides inherited implementation.

        Args:
            parent (component): parent of to_port //CHECK
            to_port (port): port that is to be connected to this port.

        Returns:
            list of semantic constraints
        """
        return {}

    def get_label(self):
        """Returns label

        Args:
            None

        Returns:
            String containing the label
        """
        return self.get_parameter("label")

    def mangle(self, name):
        """Mangles the label parameter

        Args:
            name (str): name of the port

        """
        label = self.label.replace("@@name@@", name)
        self.set_parameter("label", label, force_literal=True) ## TODO: this shouldn't require force_literal=True
