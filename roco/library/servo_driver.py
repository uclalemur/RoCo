from roco.library.driver import Driver
from roco.derived.ports import *
from roco.api.component import Component
from roco.derived.ports.pwm_port import PWMInputPort, PWMOutputPort 
from roco.derived.ports.electrical_port import ElectricalPort
from roco.derived.ports.digital_port import DigitalInputPort
from roco.derived.ports.bool_port import InBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.components.electrical_component import ElectricalComponent
from roco.derived.composables.target.arduino_target import Arduino

# from svggen.api.composables.ElectricalComposable import ElectricalComposable


class ServoDriver(Driver):
    def __init__(self, yaml_file=None, **kwargs):
        Driver.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        self.pmap = [None, None, "Pin"]

        self.physical = {
            "numPins": 3,
            "power": {
                "Vin": [0],
                "Ground": [1]
            },
            "aliases": ["Vin", "ground", "PWMin"]
        }

        self.meta = {
            Arduino: {
                "code": "",

                "inputs": {
                    "in_@@name@@": None,
                    "enable_@@name@@": None,
                },

                "outputs": {
                    "servo_@@name@@": "servo_@@name@@.write(<<in_@@name@@>>)"
                },

                "declarations": "Servo servo_@@name@@;",

                "setup": "    servo_@@name@@.attach(<<Pin_@@name@@>>);\n",

                "needs": set(["Servo.h"])
            }
        }

        self.add_interface("inInt", InIntPort(self, "inInt", "in_@@name@@"))
        self.add_interface("eOut", ElectricalPort(self, [2], virtual=True))
        self.add_interface("PWMin", PWMInputPort(self, [2], virtual=True))
        self.add_interface("Enable", InBoolPort(self, "enable", "enable_@@name@@"))
        self.add_parameter("Pin", "", isSymbol=False)

        Driver.define(self)

if __name__ == '__main__':
    a = ServoDriver(name="sd1")
    a.make_output()
