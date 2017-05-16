from roco.derived.ports.string_port import InStringPort, OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.targets.cpp_target import Cpp

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
            }
        }
        self.add_interface("outStr", OutStringPort(self, "outStr", "str@@name@@"))
        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)

if __name__ == "__main__":
    ss = StringSource()
