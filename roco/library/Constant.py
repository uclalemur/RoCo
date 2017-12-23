from roco.derived.composables.target.arduino_target import Arduino
from roco.derived.components.code_component import CodeComponent
from roco.derived.ports import *

class Constant(CodeComponent):

	def __init__(self,  yaml_file=None, name="Constant", **kwargs):
		CodeComponent.__init__(self, yaml_file, name, **kwargs)
		name = self.get_name()

	def define(self, **kwargs):
		self.add_parameter("num", 0, is_symbol=False)
		self.meta = {
			Arduino: {
				"code": ""				,

				"inputs": {
				},

				"outputs": {
					"num@@name@@" : "@@param@@num@@",
				},

				"declarations": "",
				"setup": (
					"\n"),
				"loop": (
					"\n"),
				"needs": set()
			},

		}

		self.add_interface("num", OutIntPort(self, "num", "num@@name@@"))
		CodeComponent.define(self, **kwargs)

	def assemble(self):
		CodeComponent.assemble(self)

if __name__ == "__main__":
	pass

