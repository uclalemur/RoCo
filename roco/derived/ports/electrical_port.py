from Port import Port


class ElectricalPort(Port):
    """A class representing an Electrical port



    """
    def __init__(self, parent, pins, virtual=False, **kwargs):
        """Creates an ElecticalPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        Port.__init__(self, parent, params={})
        self.pins = pins
        self.virtual = virtual
        self.parentName = parent.getName()

    def get_component_name(self):
        """Returns name of component

        Args:
            None

        """
        return self.parentName

    def getPins(self):
        """Returns an array of the pins.

        Args:
            None

        Returns:
            integer array of all pins in this port.

        """
        if isinstance(self.pins[0], int):
            return self.pins
        return self.parent.getPinIndices(self.pins)

    def isVirtual(self):
        """Returns whether or not this port is virtual

        Args:
            None

        Returns:
            Boolean

        """
        return self.virtual
