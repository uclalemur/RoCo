# Import any necessary ports. Inputs to this component will be InPorts, and
# outputs to this component should be through OutPorts. All ports are in
# roco.derived.ports
from roco.derived.ports.serial_port import OutSerialPort
from roco.derived.ports.int_port import InIntPort
from roco.derived.ports.bool_port import OutBoolPort

# Import CodeComponent if you are making a Code Component. Otherwise, import
# whatever type of component you are making.
from roco.derived.components.code_component import CodeComponent

# Import whatever kind of outputs you want to support.
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino


# Subclass this component with from Whatever type of component it is.
class SerialIn(CodeComponent):

    # This generally shouldn't change other than modifying CodeComponent to
    # whatever is appropriate
    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    # This is where the meat of your code will go. You will only be modifying
    # the self.meta dictionary. For all the code you specify in the meta parameter,
    # relative order within components is maintained but absolute ordering between
    # components is undefined.
    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            # Each key is the kind of output you support, in this case this module
            # supports only Arduino output.
            Arduino: {
                # "code" is a string containing any generic code you want. It will
                # be in the global scope, below all declarations. Generally, it
                # contains functions that will be used elsewhere in the code.
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
                # "declarations" contains all declarations for global variables
                # and functions used in the code.
                "declarations": ("void @@name@@();\n"
                                "char* @@name@@_received;\n"
                                "int @@name@@_receivedLength = 32;\n"
                                "int @@name@@_bitcounter = 0;\n"
                                "char @@name@@_prefix[4];\n"
                                "bool @@name@@_came = false;\n"),
                # "setup" contains all the code you want to be in setup. The
                # indentation is sketchy but it shouldn't matter.
                "setup": ("Serial.begin(<<inBaudRate_@@name@@>>);\n"
                        "@@name@@_received = calloc(32, sizeof(char));\n"),
                # "loop" contains all the code you want to be in the loop function.
                "loop": "@@name@@();\n",
                # "inputs" is a dictionary containing all the inputs to the component.
                # The key is the name you want to refer to the input by in the code.
                # Use it in the code as a variable as long as the type matches.
                # Wherever its used in the code, surround it with  << and >>
                # I think the value is always None, but I have to double check
                "inputs": {
                    "inBaudRate_@@name@@": None
                },
                # "outputs" is a dictionary containing all the outputs to the component.
                # The key is an arbitrary tag you call it by but it should be the same
                # lable in the definition of the ports below. The values are the
                # names of the variables that contain the value of the outputs.
                "outputs": {
                    "receivedString_@@name@@": "@@name@@_received",
                    "hasReceivedString_@@name@@": "@@name@@_came",
                },
                # "needs" is an array of any dependencies (libraries) that the
                # may use.
                "needs": set(),
                # "interface" is used to create UI stuff, I have no idea how it works
                # Don't screw with it
                "interface": {
                    "html": "",
                    "style": "",
                    "js": "",
                    "event": "",
                }
            }
        }

        # This is where you add ports to the component. The first argument is the name
        # of the port. Keep this simple and not scary because its what the users
        # will see in the blockly interface. The second argument is a port object.
        # Look at the port documentation to see how to create one.
        self.add_interface("baudRate", InIntPort(self, "baudRate", "inBaudRate_@@name@@"))
        self.add_interface("received", OutSerialPort(self, "received", "receivedString_@@name@@"))
        self.add_interface("came", OutBoolPort(self, "came", "hasReceivedString_@@name@@"))

        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


# This is optional, it lets you create the object in this file, but you can also
 # do it in the builder file.
if __name__ == "__main__":
    ss = SerialIn()
    ss.make_output()
