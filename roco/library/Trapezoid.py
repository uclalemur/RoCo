from roco.derived.components.folded_component import FoldedComponent
from roco.derived.composables.fegraph.face import Trapezoid as Trap
from roco.derived.ports.edge_port import EdgePort
from roco.derived.ports.face_port import FacePort
from roco.utils.utils import prefix
from sympy import LessThan


class Trapezoid(FoldedComponent):

    _test_params = {
        'a': 300,
        'b': 400,
        'c': 500
    }

    def define(self, **kwargs):
        FoldedComponent.define(self, **kwargs)

        self.add_parameter("h", 200, positive=True)
        self.add_parameter("l2", 300, positive=True)
        self.add_parameter("l1", 500, positive=True)


    def assemble(self):
        h = self.get_parameter("h")
        l1 = self.get_parameter("l2")
        l2 = self.get_parameter("l1")

        self.add_face(Trap("tr", l1, l2, h))

        self.place()

        self.add_interface("face", FacePort(self, "tr"))
        self.add_interface("t", EdgePort(self, "e1"))
        self.add_interface("b", EdgePort(self, "e3"))

    if __name__ == "__main__":
        h = Trapezoid()
