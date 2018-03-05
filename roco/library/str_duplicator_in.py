from roco.derived.ports.string_port import InStringPort
from roco.derived.ports.string_port import OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class StrDuplicatorIn(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "stringa")
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@param@@variable_name@@ = <<inStr_@@name@@>>;\n"
					"}\n"),
				"declarations": "char* @@param@@variable_name@@;\n",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {
					"inStr_@@name@@": None,
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
		self.add_interface("inStr", InStringPort(self, "inStr", "inStr_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = StrDuplicatorIn()
	ss.make_output()

