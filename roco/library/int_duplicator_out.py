from roco.derived.ports.int_port import InIntPort
from roco.derived.ports.int_port import OutIntPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class IntDuplicatorOut(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "numero")
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@name@@_outInt = @@param@@variable_name@@\n"
					"}\n"),
				"declarations":"",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {},
				"outputs": {
					"outInt_@@name@@": "@@name@@_outInt"
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
		self.add_interface("outInt", OutIntPort(self, "outInt", "outInt_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = IntDuplicatorOut()
	ss.make_output()

