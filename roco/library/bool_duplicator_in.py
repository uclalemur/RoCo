from roco.derived.ports.bool_port import InBoolPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class BoolDuplicatorIn(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "booleano")
		boolean = str(self.get_parameter("variable_name").get_value())
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@param@@variable_name@@ = <<inBool_@@name@@>>;\n"
					"}\n"),
				"declarations":"bool @@param@@variable_name@@;\n",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {
					"inBool_@@name@@": None,
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
		self.add_interface("inBool", InBoolPort(self, "inBool", "inBool_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = BoolDuplicatorIn()
	ss.make_output()

