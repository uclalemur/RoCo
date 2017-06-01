from roco.derived.ports.serial_port import OutSerialPort
from roco.derived.ports.int_port import InIntPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class SerialIn(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code": ("void @@name@@(){\n"
                        "\t@@name@@_bitcounter = 0;\n"
                        "\twhile(Serial.available()){\n"
                        "\t\tif(@@name@@_bitcounter < @@name@@_receivedLength){"
                        "\t\t\t@@name@@_received[@@name@@_bitcounter] = tolower(Serial.read());\n"
                        "\t\t\t@@name@@_bitcounter++;\n"
                        "\t\t\t@@name@@_came = true;\n"
                        "\t\t\tdelay(10);\n"
                        "\t\t}\n"
                        "\t\telse{\n"
                        "\t\t\t@@name@@_received = realloc(@@name@@_received, @@name@@_receivedLength*2);\n"
                        "\t\t\t@@name@@_receivedLength = @@name@@_receivedLength*2;\n"
                        "\t\t}\n"
                        "\t}\n"
                        "}\n"),
                "declarations": ("void @@name@@();\n"
                                "char* @@name@@_received;\n"
                                "int @@name@@_receivedLength = 32;\n"
                                "int @@name@@_bitcounter = 0;\n"
                                "char @@name@@_prefix[4];\n"
                                "bool @@name@@_came = false;\n"),
                "setup": ("Serial.begin(<<inBaudRate_@@name@@>>);\n"
                        "@@name@@_received = calloc(32, sizeof(char));\n"),
                "loop": "@@name@@();\n",
                "inputs": {
                    "inBaudRate_@@name@@": None
                },
                "outputs": {
                    "receivedString_@@name@@": "@@name@@_received"
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

        self.add_interface("baudRate", InIntPort(self, "baudRate", "inBaudRate_@@name@@"))
        self.add_interface("received", OutSerialPort(self, "received", "receivedString_@@name@@"))

        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = SerialIn()
    ss.make_output()
