from roco.api.port import Port


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
        self.parent_name = parent.get_name()

    def get_component_name(self):
        """Returns name of component

        Args:
            None

        """
        return self.parent_name

    def get_pins(self):
        """Returns an array of the pins.

        Args:
            None

        Returns:
            integer array of all pins in this port.

        """
        if isinstance(self.pins[0], int):
            return self.pins
        return self.parent.get_pin_indices(self.pins)

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

    def is_virtual(self):
        """Returns whether or not this port is virtual

        Args:
            None

        Returns:
            Boolean

        """
        return self.virtual
