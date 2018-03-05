from roco.derived.components.folded_component import FoldedComponent
from roco.derived.composables.fegraph.face import Triangle as Tri
from roco.derived.ports.edge_port import EdgePort
from roco.derived.ports.face_port import FacePort


class Triangle(FoldedComponent):

    _test_params = {
        'a': 300,
        'b': 400,
        'c': 200
    }

    def define(self, **kwargs):
        FoldedComponent.define(self, **kwargs)

        self.add_parameter("a", 300, positive=True)
        self.add_parameter("b", 250, positive=True)
        self.add_parameter("c", 200, positive=True)
        da = self.get_parameter("a")
        db = self.get_parameter("b")
        dc = self.get_parameter("c")
        self.add_constraint(da <  db + dc)
        self.add_constraint(db <  dc + da)
        self.add_constraint(dc <  da + db)

    def assemble(self):
        da = self.get_parameter("a")
        db = self.get_parameter("b")
        dc = self.get_parameter("c")

        self.add_face(Tri("t", da, db, dc))

        self.place()

        self.add_interface("face", FacePort(self, "t"))
        self.add_interface("b", EdgePort(self, "e0"))
        self.add_interface("a", EdgePort(self, "e1"))
        self.add_interface("c", EdgePort(self, "e2"))

if __name__ == "__main__":
    h = Triangle()
