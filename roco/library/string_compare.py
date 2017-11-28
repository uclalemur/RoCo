from roco.derived.ports.string_port import InStringPort
from roco.derived.ports.bool_port import InBoolPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class StringCompare(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code": ("void @@name@@(){\n"
                        "\tif(<<hasReceivedSerial_@@name@@>>){\n"
                        "\t\tif(strcmp(<<inString_@@name@@>>, @@string@@) == 0){\n"
                        "\t\t\t@@name@@_isMatch = 1;\n"
                        "\t\t}\n"
                        "\t}\n"
                        "}\n"),
                "declarations": "bool @@name@@_isMatch = 0;\n",
                "setup": "",
                "loop": "@@name@@();\n",
                "inputs": {
                    "inString_@@name@@": None,
                    "hasReceivedSerial_@@name@@": None,
                },
                "outputs": {
                    "isMatch_@@name@@": "@@name@@_isMatch"
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
        self.add_interface("inString", InStringPort(self, "inString", "inString_@@name@@"))
        self.add_interface("inDetected", InBoolPort(self, "inDetected", "hasReceivedSerial_@@name@@"))
        self.add_interface("isMatch", OutBoolPort(self, "isMatch", "isMatch_@@name@@"))
        self.add_parameter("compareString", "Go")


        CodeComponent.define(self, **kwargs)

    def assemble(self):
        cmpString =  str(self.get_parameter("compareString"))
        (self.meta.get(Arduino).get("code")).replace("@@string@@", cmpString)
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = StringCompare()
    ss.make_output()
