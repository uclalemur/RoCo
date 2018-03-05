from roco.derived.ports.virtual_electrical_port import VirtualElectricalPort


class PWMInputPort(VirtualElectricalPort):
    """A PWM input port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False,  **kwargs):
        """Creates a PWMInputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.add_allowable_mate(PWMOutputPort)

class PWMOutputPort(VirtualElectricalPort):
    """A PWM output port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False,  **kwargs):
        """Creates a PWOutputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.add_allowable_mate(PWMInputPort)

if __name__ == "__main__":
    pass
    