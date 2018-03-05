from roco.derived.ports.serial_port import InSerialPort
from roco.derived.ports.string_port import OutStringPort
from roco.derived.ports.bool_port import InBoolPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino


class SerialToString(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code": ("void @@name@@(){\n"
                        "\tif(<<hasReceivedSerial_@@name@@>>){\n"
                        "\t\t@@name@@_receivedString = (char*)<<receivedSerial_@@name@@>>;\n"
                        "\t\t@@name@@_cameOut = true;\n"
                        "\t}\n"
                        "}\n"),
                "declarations": ("void @@name@@();\n"
                                "char* @@name@@_receivedString;\n"
                                "bool @@name@@_cameOut = false;\n"),
                "setup": "",
                "loop": "@@name@@();\n",
                "inputs": {
                    "receivedSerial_@@name@@": None,
                    "hasReceivedSerial_@@name@@": None,
                },
                "outputs": {
                    "receivedString_@@name@@": "@@name@@_receivedString",
                    "hasReceivedString_@@name@@": "@@name@@_cameOut",
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
        self.add_interface("received", InSerialPort(self, "received", "receivedSerial_@@name@@"))
        self.add_interface("came", InBoolPort(self, "came", "hasReceivedSerial_@@name@@"))
        self.add_interface("receivedString", OutStringPort(self, "receivedString_out", "receivedString_@@name@@"))
        self.add_interface("cameOut", OutBoolPort(self, "cameOut", "hasReceivedString_@@name@@"))

        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = SerialToString()
    ss.make_output()
