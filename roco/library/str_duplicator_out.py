from roco.derived.ports.string_port import InStringPort
from roco.derived.ports.string_port import OutStringPort
from roco.derived.components.code_component import CodeComponent
from roco.derived.composables.target.cpp_target import Cpp
from roco.derived.composables.target.arduino_target import Arduino

class StrDuplicatorOut(CodeComponent):

	def __init__(self, yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)

	def define(self, **kwargs):
		name = self.get_name()
		self.add_parameter("variable_name", "stringa")
		self.meta = {
			Arduino: {
				"code": ("void @@name@@(){\n"
					"\t@@name@@_outStr = @@param@@variable_name@@;\n"
					"}\n"),
				"declarations":"char* @@name@@_outStr;\n",
				"setup": "",
				"loop": "\t@@name@@();\n",
				"inputs": {},
				"outputs": {
					"outStr_@@name@@": "@@name@@_outStr"
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
		self.add_interface("outStr", OutStringPort(self, "outStr", "outStr_@@name@@"))


		CodeComponent.define(self, **kwargs)

	def assemble(self):
		#print self.get_parameter("variable_name").get_value()
		CodeComponent.assemble(self)


if __name__ == "__main__":
	ss = IntDuplicatorOut()
	ss.make_output()

