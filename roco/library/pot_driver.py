from roco.library.driver import Driver
from roco.derived.composables.target.arduino_target import Arduino
from roco.derived.composables.electrical_composable import ElectricalComposable
from roco.derived.ports.electrical_port import ElectricalPort
from roco.derived.ports.analog_port import AnalogOutputPort
from roco.derived.ports.int_port import OutIntPort

class PotDriver(Driver):

    def __init__(self, yaml_file=None, **kwargs):
        Driver.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        Driver.define(self, **kwargs)

        self.physical = {
            "numPins": 3,
            "power": {
                "Vin": [0],
                "Ground": [2]
            },
            "aliases": ["first pin", "center pin", "last pin"],
        }

        self.pmap = [None, "pin", None]

        self.add_parameter("pin", "", is_symbol=False)

        self.meta = {
            Arduino: {
                "code": "",

                "inputs": {
                },

                "outputs": {
                    "analog@@name@@": "analogRead(<<pin_@@name@@>>)"
                },

                "declarations": "",
                "setup": "",
                "needs": set()
            }
        }
        self.add_interface("vIn", ElectricalPort(self, [1], virtual=True))
        self.add_interface("aOut", AnalogOutputPort(self, [1], virtual=True))
        self.add_interface("outInt", OutIntPort(self, "outInt", "analog@@name@@"))

if __name__ == '__main__':
    a = PotDriver(name="pot_driver1")
    a.make_output()
