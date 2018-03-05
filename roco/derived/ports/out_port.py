"""OutPort class.

This module contains the OutPort class.

"""

from roco.api.port import Port
from in_port import InPort

class OutPort(CodePort):
    """A class representing an output port.

    Attributes:
        No new attributes.

    """
    def __init__(self, parent, name, **kwargs):
        """Creates an OutPort object.

        Args:
            parent (component): The component to which this port will be added.
            name (str): name of the port.
            kwargs (dict): additional arguments to override params.
        """
        Port.__init__(self, parent, {}, name, **kwargs)
        self.add_allowable_mate(self.__class__)

    def can_mate(self, other_port):
        """Returns true if this port can mate with other_port and false otherwise.
        Overrides inherited implementation

        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are compatible.
        """
        if self.type is None or other_port.type is None:
            return isinstance(other_port, InPort)
        return (self.type == other_port.type) and isinstance(other_port, InPort)

if __name__ == "__main__":
    pass
    