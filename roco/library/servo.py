from roco.derived.ports.electrical_port import ElectricalPort
from roco.derived.components.electrical_component import ElectricalComponent


class Servo(ElectricalComponent):

    def __init__(self, yaml_file=None, **kwargs):
        ElectricalComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        ElectricalComponent.define(self)

        self.physical =  {
            "numPins": 3,
            "power": {
                "Vin": [1],
                "Ground": [0]
            },
            "aliases": ["Vin", "ground", "PWMin"]
        }

        self.add_interface('eIn', ElectricalPort(self, [2]))

    def assemble(self):
        ElectricalComponent.assemble(self)

if __name__ == '__main__':
    a = Servo(name="sd1")
    a.make_output()