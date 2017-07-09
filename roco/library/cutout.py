from roco.api.component import Component
from roco.derived.composables.graph_composable import Decoration
from roco.derived.composables.fegraph.face import Face
from roco.derived.ports.mount_port import MountPort



class Cutout(Component):

  def define(self):
      self.add_parameter("width", 60)
      self.add_parameter("length", 135)
      self.add_interface("mount", MountPort(self, None))

  def assemble(self):
    w = self.get_parameter("width").get_value()
    l = self.get_parameter("length").get_value()

    dx = w/2.0
    dy = l/2.0
    hole = Face("hole", ((-dx, -dy), (dx, -dy), (dx, dy), (-dx, dy)), recenter=False)

    graph = Decoration()
    graph.add_face(hole, prefix="hole")
    self.set_interface("mount", MountPort(self, graph))

if __name__ == "__main__":
    h = Header()
    h.set_parameter("width", 11)
    h.set_parameter("length", 11)
    h.make()
