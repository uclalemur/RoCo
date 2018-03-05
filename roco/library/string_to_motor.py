from roco.derived.ports.string_port import InStringPort
from roco.derived.ports.bool_port import InBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino


class StringToMotor(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code": ("void @@name@@(){\n"
                        "\tif(<<hasReceivedSerial_@@name@@>>){\n"
                        "\t\tif(strcmp(<<motorInstruction_@@name@@>>, \"go\") == 0){\n"
                        "\t\t\t@@name@@_left.write(0);\n"
                        "\t\t\t@@name@@_right.write(180);\n"
                        "\t\t}\n"
                        "\t\telse if(strcmp(<<motorInstruction_@@name@@>>, \"stop\") == 0){\n"
                        "\t\t\t@@name@@_left.write(90);\n"
                        "\t\t\t@@name@@_right.write(90);\n"
                        "\t\t}\n"
                        "\t\tfor(int i = 0; <<motorInstruction_@@name@@>>[i] != 0; i++){\n"
                        "\t\t\t<<motorInstruction_@@name@@>>[i] = 0;\n"
                        "\t\t}\n"
                        "\t}\n"
                        "}\n"),
                "declarations": ("#include <Servo.h>\n"
                                "Servo @@name@@_right;\n"
                                "Servo @@name@@_left;\n"),
                "setup": ("\t@@name@@_left.attach(5);\n"
                          "\t@@name@@_right.attach(4);\n"),
                "loop": "@@name@@();\n",
                "inputs": {
                    "motorInstruction_@@name@@": None,
                    "hasReceivedSerial_@@name@@": None,
                },
                "outputs": {},
                "needs": set(),
                "interface": {
                    "html": "",
                    "style": "",
                    "js": "",
                    "event": "",
                }
            }
        }
        self.add_interface("motorString", InStringPort(self, "motorString", "motorInstruction_@@name@@"))
        self.add_interface("motorCame", InBoolPort(self, "motorCame", "hasReceivedSerial_@@name@@"))


        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = StringToMotor()
    ss.make_output()
