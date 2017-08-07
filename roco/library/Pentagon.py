from roco.derived.components.folded_component import FoldedComponent
from roco.derived.composables.fegraph.face import Pentagon as Penta
from roco.derived.ports.edge_port import EdgePort
from roco.derived.ports.face_port import FacePort

class Pentagon(FoldedComponent):

    _test_params = {
        'a': 100
    }

    def define(self, **kwargs):
        FoldedComponent.define(self, **kwargs)
        self.add_parameter("s", 200, positive=True)

    def assemble(self):
        s = self.get_parameter("s")

        self.add_face(Penta("pe", s))

        self.place()

        self.add_interface("face", FacePort(self, "pe"))
        self.add_interface("s1", EdgePort(self, "e1"))
        self.add_interface("s2", EdgePort(self, "e2"))
        self.add_interface("s3", EdgePort(self, "e3"))
        self.add_interface("s4", EdgePort(self, "e4"))
        self.add_interface("s5", EdgePort(self, "e5"))

    if __name__ == "__main__":
        h = Pentagon()
