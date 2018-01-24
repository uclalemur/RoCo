from roco.derived.ports.int_port import InIntPort
from roco.derived.ports.int_port import OutIntPort
from roco.derived.ports.bool_port import InBoolPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class FtoIntMultiplexer(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Arduino: {
                "code": ("void @@name@@(){\n"
                        "\tif(<<switchOne_@@name@@>>)\n"
                        "\t{\n"
                        "\t\t@@name@@_output = <<inputOne_@@name@@>>;\n"
                        "\t}\n"
                        "\telse if(<<switchTwo_@@name@@>>)\n"
                        "\t{\n"
                        "\t\t@@name@@_output = <<inputTwo_@@name@@>>;\n"
                        "\t}\n"
                        "\telse if(<<switchThree_@@name@@>>)\n"
                        "\t{\n"
                        "\t\t@@name@@_output = <<inputThree_@@name@@>>;\n"
                        "\t}\n"
                        "\telse if(<<switchFour_@@name@@>>)\n"
                        "\t{\n"
                        "\t\t@@name@@_output = <<inputFour_@@name@@>>;\n"
                        "\t}\n"
                        "}\n"),
                "declarations": "int @@name@@_output;\n",
                "setup": "",
                "loop": "\t@@name@@();\n",
                "inputs": {
                    "inputOne_@@name@@": None,
                    "inputTwo_@@name@@": None,
                    "inputThree_@@name@@": None,
                    "inputFour_@@name@@": None,
                    "switchOne_@@name@@": None,
                    "switchTwo_@@name@@": None,
                    "switchThree_@@name@@": None,
                    "switchFour_@@name@@": None,
                },
                "outputs": {
                    "output_@@name@@": "@@name@@_output"
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
        self.add_interface("inputOne", InIntPort(self, "inputOne", "inputOne_@@name@@"))
        self.add_interface("inputTwo", InIntPort(self, "inputTwo", "inputTwo_@@name@@"))
        self.add_interface("inputThree", InIntPort(self, "inputThree", "inputThree_@@name@@"))
        self.add_interface("inputFour", InIntPort(self, "inputFour", "inputFour_@@name@@"))
        self.add_interface("switchOne", InBoolPort(self, "switchOne", "switchOne_@@name@@"))
        self.add_interface("switchTwo", InBoolPort(self, "switchTwo", "switchTwo_@@name@@"))
        self.add_interface("switchThree", InBoolPort(self, "switchThree", "switchThree_@@name@@"))
        self.add_interface("switchFour", InBoolPort(self, "switchFour", "switchFour_@@name@@"))
        self.add_interface("output", OutIntPort(self, "output", "output_@@name@@"))
        
        


        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
	#c = Component(name = 'fto_int_multiplexer')
	ss = FtoIntMultiplexer()
	#c.to_yaml("library/fto_int_multiplexer.yaml")
	ss.make_output()
