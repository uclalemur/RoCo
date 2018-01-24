from roco.derived.ports.bool_port import InBoolPort
from roco.derived.ports.bool_port import OutBoolPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class BoolDuplicatorOut(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "booleano")
		boolean = str(self.get_parameter("variable_name").get_value())
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@name@@_outBool = @@param@@variable_name@@;\n"
					"}\n"),
				"declarations":"bool @@name@@_outBool;\n",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {},
				"outputs": {
					"outBool_@@name@@": "@@name@@_outBool"
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
		self.add_interface("outBool", OutBoolPort(self, "outBool", "outBool_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = BoolDuplicatorOut()
	ss.make_output()

