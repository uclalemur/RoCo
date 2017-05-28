"""
class Button(ElectricalComponent):

    def __init__(self, yamlFile=None, **kwargs):
        ElectricalComponent.__init__(self, yamlFile, **kwargs)

    def define(self, **kwargs):
        self.physical = {
            "pin1": None,
            "pin2": None
        }

        self.addInterface("ein", ElectricalPort(self, "ein", ["pin1"]))
        self.addInterface("eout", ElectricalPort(self, "eout", ["pin2"]))

        ElectricalComponent.define(self)


    def assemble(self):
        ElectricalComponent.assemble(self)

"""
from roco.derived.components.electrical_component import ElectricalComponent
from roco.derived.ports.electrical_port import ElectricalPort
import pdb

class Button(ElectricalComponent):

    def define(self, **kwargs):
        ElectricalComponent.define(self)

        self.set_parameter("physical", {
            "name": self.get_name(),
            "numPins": 2,
            "power": {
                "Vin": [0],
                "Ground": [1],
                "pullDown": self.get_parameter("pulldown"),
                "pullUp": self.get_parameter("pullup")
            }
        }, force_literal=True)

        self.add_interface("ein", ElectricalPort(self, self.get_name(), [0]))
        self.add_interface("eout", ElectricalPort(self, self.get_name(), [1]))

if __name__ == '__main__':
    a = Button(name="button1")
    a.make_output()
