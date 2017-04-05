from roco.derived.ports.virtual_electrical_port import VirtualElectricalPort

class AnalogInputPort(VirtualElectricalPort):
    """An Analog input port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False, **kwargs):
        """Creates an AnalogInputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.addAllowableMate(AnalogOutputPort)

class AnalogOutputPort(VirtualElectricalPort):
    """An Analog output port.

    Attributes:
        None
    """
    def __init__(self, parent, pin, virtual=False,  **kwargs):
        """Creates an AnalogOuputPort Object

        Args:
            parent (component): The component to which this port will be added.
            pins (int array): Array containing the pins in this electrical port.
            virtual (Boolean): Whether or not the port is virtual.
            kwargs (dict): additional arguments to override params.

        """
        VirtualElectricalPort.__init__(self, parent, pin, virtual, **kwargs)
        self.addAllowableMate(AnalogInputPort)
