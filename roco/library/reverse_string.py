from roco.derived.ports.string_port import InStringPort, OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino


class ReverseString(CodeComponent):

    def __init__(self, yaml_file=None, **kwargs):
        CodeComponent.__init__(self, yaml_file, **kwargs)

    def define(self, **kwargs):
        name = self.get_name()
        self.meta = {
            Cpp: {
                "code": "std::string @@name@@(std::string str)\n" + \
                    "{\n" + \
                    "    size_t len = str.length();\n\n" + \
                    "    for (int i = 0;i < len / 2;++i)\n" + \
                    "    {\n" + \
                    "        char c = str[i];\n" + \
                    "        str[i] = str[len - i - 1];\n" + \
                    "        str[len - i - 1] = c;\n" + \
                    "    }\n\n" + \
                    "    return str;\n" + \
                    "}\n",

                "inputs": {
                    "inReverse_@@name@@": None
                },

                "outputs": {
                    "reversed_@@name@@": "@@name@@(<<inReverse_@@name@@>>)"
                },

                "declarations": "@@name@@(std::string str);\n",

                "needs": set()
            },
            Arduino: {
                "code": "std::string @@name@@(std::string str)\n" + \
                    "{\n" + \
                    "    size_t len = str.length();\n\n" + \
                    "    for (int i = 0;i < len / 2;++i)\n" + \
                    "    {\n" + \
                    "        char c = str[i];\n" + \
                    "        str[i] = str[len - i - 1];\n" + \
                    "        str[len - i - 1] = c;\n" + \
                    "    }\n\n" + \
                    "    return str;\n" + \
                    "}\n",
                "declarations": "@@name@@(std::string str);\n",
                "setup": "",
                "loop": "",
                "inputs": {
                    "inReverse_@@name@@": None
                },
                "outputs": {
                    "reversed_@@name@@": "@@name@@(<<inReverse_@@name@@>>)"
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

        self.add_interface("inStr", InStringPort(self, "inStr", "inReverse_@@name@@"))
        self.add_interface("outStr", OutStringPort(self, "reversed", "reversed_@@name@@"))

        CodeComponent.define(self, **kwargs)

    def assemble(self):
        CodeComponent.assemble(self)


if __name__ == "__main__":
    ss = ReverseString()
