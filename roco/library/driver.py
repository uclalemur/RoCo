from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.electrical_composable import ElectricalComposable


class Driver(CodeComponent):
    def __init__(self, yaml_file=None, **kwargs):
        self.pmap = []
        self.physical = {
            "numPins": 0,
            "power": {
                "Vin": [],
                "Ground": []
            },
            "aliases": []
        }
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def get_pin_alias(self, pin):
        if not isinstance(pin, list):
            return [self.pmap[pin]]
        if isinstance(pin[0], int):
            return [self.pmap[i] for i in pin]
        return pin

    def set_pin_parameter(self, pin_names, pin_values):
        if isinstance(pin_names, list):
            for (pin_name, pin_value) in zip(pin_names, pin_values):
                self.set_parameter(pin_name, pin_value, force_literal=True)
        else:
            self.set_parameter(pin_names, pin_values, force_literal=True)

    def get_token_subs(self):
        return dict([(key + "_" + self.get_modified_name(), str(val)) for key, val in self.parameters.iteritems()])

    def assemble(self):
        self.composables['electrical'] = ElectricalComposable(self.get_name(), self.physical, is_virtual=True)
        CodeComponent.assemble(self)
