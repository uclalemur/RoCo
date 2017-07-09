from roco.api.component import Component
from roco.derived.ports.analog_port import AnalogInputPort
from roco.derived.ports.digital_port import DigitalInputPort, DigitalOutputPort
from roco.derived.ports.pwm_port import PWMOutputPort
from roco.derived.composables.container_composable import ContainerComposable
from roco.derived.composables.code_container import CodeContainer
from roco.derived.composables.electrical_container import ElectricalContainer
from roco.derived.composables.electrical_composable import ElectricalComposable


class NodeMcu(Component):

    def define(self, **kwargs):
        self.pin_indices = dict()

        for n in range(0, 1):
            self.add_interface("a%d" % (n+1), AnalogInputPort(self, ["A%d" % n]))
            self.add_parameter("A%d" % n, n, is_symbol=False)
            self.pin_indices["A%d" % n] = n + 9

        for n in range(0, 9):
            self.add_interface("di%d" % n, DigitalInputPort(self,["D%d" % n]))
            self.add_interface("do%d" % n, DigitalOutputPort(self,["D%d" % n]))
            self.pin_indices["D%d" % n] = n
            self.add_parameter("D%d" % n, n, is_symbol=False)

    def set_pin_parameter(self, pin_name, pin_value):
        pass

    def get_pin_indices(self, pins):
        return [self.pin_indices[i] for i in pins]

    def get_pin_alias(self, pin):
        if not isinstance(pin, list):
            return [str(pin)]
        if isinstance(pin[0], int):
            return [str(i) for i in pin]
        return pin

    def assemble(self):
        #self.composables['code'] = CodeContainer()
        #self.composables['electrical'] = ElectricalContainer(self.getName(), 19)
        self.composables['electrical'] = ElectricalComposable(self.get_name(), {
                "numPins": 10,
                "power": {
                    "Vin": [],
                    "Ground": [],
                },
                "aliases": ["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "A0"]
            })

if __name__ == '__main__':
    a = NodeMcu(name="nmcu")
    print a.parameters
    # a.make_output()
