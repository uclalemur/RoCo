from roco.derived.ports.electrical_port import ElectricalPort

class VirtualElectricalPort(ElectricalPort):
    """NO IDEA WHAT ANYTHING IN THIS FILE DOES

    Args:
        None

    """
    def __init__(self, parent, pin, virtual=False, **kwargs):
        ElectricalPort.__init__(self, parent, pin, virtual, **kwargs)

    def get_pin_alias(self, p):
        """NO IDEA WHAT THIS DOES

        Args:
            p

        """
        return self.parent.get_pin_alias(p)

    def set_parent_pin(self, pval):
        """Set value of parent pin to pval

        Args:
            pval (int) : new value of parent pin

        """
        self.parent.set_pin_parameter(self.get_pin_alias(self.pins), pval)

    def constrain(self, parent, to_port, **kwargs):
        to_port.set_parent_pin(self.get_pin_alias(self.pins))
        self.set_parent_pin(to_port.get_pin_alias(to_port.pins))
        return []

if __name__ == "__main__":
    pass
    