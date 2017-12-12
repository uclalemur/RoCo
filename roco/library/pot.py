from roco.derived.components.electrical_component import ElectricalComponent
from roco.derived.ports.analog_port import AnalogOutputPort

class Pot(ElectricalComponent):

    def __init__(self, yamlFile=None, **kwargs):
        ElectricalComponent.__init__(self, yamlFile, **kwargs)

    def define(self, **kwargs):
        ElectricalComponent.define(self)
        self.physical = {
            "numPins": 3,
            "power": {
                "Vin": [0],
                "Ground": [2]
            },
            "aliases": ["first pin", "center pin", "last pin"],
        }
        self.add_interface("vOut", AnalogOutputPort(self, [1]))


    def assemble(self):
        ElectricalComponent.assemble(self)

if __name__ == '__main__':
    a = Pot(name="pot1")
    a.make_output()
