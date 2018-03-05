from roco.derived.components.folded_component import FoldedComponent
from roco.derived.composables.fegraph.face import Rectangle as Rect 
from roco.derived.composables.graph_composable import GraphComposable
from roco.derived.ports.edge_port import EdgePort
from roco.derived.ports.face_port import FacePort
# import pdb

class Rectangle(FoldedComponent):

    _test_params = {
        'l': 100,
        'w': 400,
    }

    def define(self, **kwargs):
        FoldedComponent.define(self, **kwargs)     ## ?  ##

        self.add_parameter("l", 400, positive=True)
        self.add_parameter("w", 100, positive=True)

    def assemble(self):
        dx = self.get_parameter("l")
        dy = self.get_parameter("w")

        self.add_face(Rect("r", dx, dy))

        self.place()

        self.add_interface("face", FacePort(self, "r"))
        self.add_interface("b", EdgePort(self, "e0"))
        self.add_interface("r", EdgePort(self, "e1"))
        self.add_interface("t", EdgePort(self, "e2"))
        self.add_interface("l", EdgePort(self, "e3"))

if __name__ == "__main__":
    # pdb.set_trace() 
    h = Rectangle()
    h.make_output()
    #h._make_test()
