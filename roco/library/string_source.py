from roco.derived.ports.string_port import OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino


class StringSource(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        self.meta = {
            Cpp: {
                "code": "",

                "inputs": {

                },

                "outputs": {
                    "str@@name@@": "\"Hello World!\\n\""
                },

                "declarations": "",

                "needs": set()
            },
            Arduino: {
                "code": "",

                "declarations": "",

                "setup": "",

                "loop": "",

                "inputs": {},

                "outputs": {
                    "str@@name@@": "\"Hello World!\\n\""
                },

                "needs": set(),

                "interface": {
                    "html": "",
                    "style": "",
                    "js": "",
                    "event": "",
                }
            }
        }
        self.add_interface("outStr", OutStringPort(self, "outStr", "str@@name@@"))
        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)

if __name__ == "__main__":
    ss = StringSource()
    ss.make_output()
