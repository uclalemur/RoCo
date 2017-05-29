from roco.derived.ports.virtual_electrical_port import VirtualElectricalPort


class DigitalInputPort(VirtualElectricalPort):
    """A Digital input port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False,  **kwargs):
        """Creates an DigitalInputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.add_allowable_mate(DigitalOutputPort)

class DigitalOutputPort(VirtualElectricalPort):
    """A Digital output port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False,  **kwargs):
        """Creates an DigitalOutputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """

        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.add_allowable_mate(DigitalInputPort)
