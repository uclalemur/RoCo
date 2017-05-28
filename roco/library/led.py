from roco.derived.components.electrical_component import ElectricalComponent
from roco.derived.ports.electrical_port import ElectricalPort
import pdb

class LED(ElectricalComponent):

    def __init__(self, yaml_file=None, name=None, **kwargs):
        ElectricalComponent.__init__(self, yaml_file, name, **kwargs)

    def define(self, **kwargs):
        ElectricalComponent.define(self)

        self.physical =  {
            "numPins": 2,
            "power": {
                "Vin": [0],
                "Ground": [1]
            },
            "aliases": ["anode", "cathode"]
        }

        self.add_interface('eIn', ElectricalPort(self, [0]))

    def assemble(self):
        ElectricalComponent.assemble(self)


if __name__ == '__main__':
    a = LED(name="led1")
    print self.parameters
    a.make_output()
