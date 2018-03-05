from roco.derived.composables.target.arduino_target import Arduino
from roco.derived.components.code_component import CodeComponent
from roco.derived.ports.int_port import OutIntPort


class UserToggle(CodeComponent):

	def __init__(self,  yaml_file=None, **kwargs):
		CodeComponent.__init__(self, yaml_file, **kwargs)
		name = self.get_name()

	def define(self, **kwargs):
		self.meta = {
			Arduino: {
				"code": ""				,

				"inputs": {
				},

				"outputs": {
					"tog@@name@@" : "@@name@@item",
				},

				"declarations": ()				,

				"setup":  "@@name@@item = (int)(0);\n" 
				,

				"loop": ( "    @@name@@item = (int)(!@@name@@item);\n" 
					"    \n" )
				,

				"needs": set()
			},

		}

		self.add_interface("tog", OutIntPort(self, "tog", "tog@@name@@"))
		CodeComponent.define(self, **kwargs)

	def assemble(self):
		CodeComponent.assemble(self)


if __name__ == "__main__":
	pass

