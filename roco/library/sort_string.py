from roco.derived.ports.string_port import InStringPort, OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp


class SortString(CodeComponent):

    def __init__(self, yaml_file=None, name = None, **kwargs):
        CodeComponent.__init__(self, yaml_file, name, **kwargs)

    def define(self, **kwargs):
        self.meta = {
            Cpp: {
                "code": "",

                "inputs": {
                    "inSort_@@name@@": None
                },

                "outputs": {
                    "sorted_@@name@@": "std::sort(<<inSort_@@name@@>>)"
                },

                "declarations": "",

                "needs": set()
            }
        }
        self.add_interface("inStr", InStringPort(self, "inStr", "inSort_@@name@@"))
        self.add_interface("outStr", OutStringPort(self, "sorted", "sorted_@@name@@"))
        CodeComponent.define(self, **kwargs)


    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = SortString()
