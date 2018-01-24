from roco.derived.ports.int_port import InIntPort
from roco.derived.ports.int_port import OutIntPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class IntDuplicatorIn(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "numero")
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@param@@variable_name@@ = <<inInt_@@name@@>>;\n"
					"}\n"),
				"declarations": "int @@param@@variable_name@@ = 0;\n",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {
					"inInt_@@name@@": None,
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
		self.add_interface("inInt", InIntPort(self, "inInt", "inInt_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = IntDuplicatorIn()
	ss.make_output()

