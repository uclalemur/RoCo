from roco.api.component import Component
from roco.derived.composables.graph_composable import Decoration
from roco.derived.composables.fegraph.face import Face
from roco.derived.ports.mount_port import MountPort


class Header(Component):

	def define(self):
		self.add_parameter("nrows", 15)
		self.add_parameter("ncols", 2)
		self.add_parameter("rowsep", 2.54)
		self.add_parameter("colsep", 23)
		self.add_parameter("diameter", 1)
		self.add_interface("mount", MountPort(self, None))

	def assemble(self):
		diam = self.get_parameter("diameter").get_value()/2.0
		nr = self.get_parameter("nrows").get_value()
		nc = self.get_parameter("ncols").get_value()

		def hole(i, j, d):
			dx = (j - (nc-1)/2.0)*self.get_parameter("colsep")
			dy = (i - (nr-1)/2.0)*self.get_parameter("rowsep")
			return Face("r-%d-%d" % (i,j), 
				((dx-d, dy-d), (dx+d, dy-d), (dx+d, dy+d), (dx-d, dy+d)), 
				recenter=False)

		graph = Decoration()
		for i in range(nr):
			for j in range(nc):
				d = diam
				if (i == 0 and j == 0) or (i == nr-1 and j == nc-1):
					d = diam*3
				graph.add_face(hole(i,j,d), prefix="r-%d-%d" % (i,j))
		self.set_interface("mount", MountPort(self, graph))

if __name__ == "__main__":
	h = Header()
	h.set_parameter("nrows", 11)
	h.set_parameter("ncols", 2)
	h.set_parameter("rowsep", 0.1 * 25.4)
	h.set_parameter("colsep", 0.6 * 25.4)
	h.make()
