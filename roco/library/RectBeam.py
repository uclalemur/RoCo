from roco.derived.components.folded_component import FoldedComponent
from roco.derived.composables.fegraph.face import Face, Rectangle
from roco.derived.ports.face_port import FacePort
from roco.derived.ports.edge_port import EdgePort
from roco.utils.utils import prefix
import roco.utils.mymath as math


class RectBeam(FoldedComponent):

    def define(self, **kwargs):
        FoldedComponent.define(self, **kwargs)
        self.add_parameter("length", 150.9, positive=True)
        self.add_parameter("width", 72.6, positive=True)
        self.add_parameter("depth", 7.7, positive=True)


        self.add_parameter("tangle", 90, is_literal=True, **kwargs)
        self.add_parameter("bangle", 90, is_literal=True, **kwargs)

        self.add_parameter("phase", 0, is_literal=True, **kwargs)

        self.add_parameter("faces", False, is_literal=True, **kwargs)

    def assemble(self):
        tangle = 90 - self.get_parameter("tangle")
        bangle = 90 - self.get_parameter("bangle")

        faces = self.get_parameter("faces")

        length = self.get_parameter("length")
        width = self.get_parameter("width")
        depth = self.get_parameter("depth")
        phase = self.get_parameter("phase")

        rs = []
        rs.append(Rectangle("", width, length))
        rs.append(Rectangle("", depth, length))
        rs.append(Rectangle("", width, length))
        rs.append(Rectangle("", depth, length))
        '''rs.append(Face("", (
            (depth, math.tan(math.deg2rad(bangle)) * depth),
            (depth, length - math.tan(math.deg2rad(tangle)) * depth),
            (0, length), (0,0)
        )))
        rs.append(Rectangle("", width, length - (math.tan(math.deg2rad(bangle)) + math.tan(math.deg2rad(tangle))) * depth))
        rs.append(Face("", (
            (0, length), (0,0),
            (depth, math.tan(math.deg2rad(tangle)) * depth),
            (depth, length - math.tan(math.deg2rad(bangle)) * depth),
        )))'''

        for i in range(phase):
            rs.append(rs.pop(0))

        from_edge = None
        for i in faces or range(4):
            self.attach_face(from_edge, rs[i], "e3", prefix="r%d"%i, angle=90)
            print self.composables['graph'].edges
            from_edge = prefix('r%d' % i,'e1')

        '''if faces is False:
            self.addTab(prefix("r0","e3"), prefix("r3","e1"), angle= 90, width=[depth, width][phase % 2])'''

        self.place()

        #Define interfaces
        for i in faces or range(4):
            self.add_interface("face%d"%i, FacePort(self, "r%d"%i))

        for i, n in enumerate(faces or range(4)):
            self.add_interface("topedge%d" % i, EdgePort(self, prefix("r%d" % n,"e0")))
            self.add_interface("botedge%d" % i, EdgePort(self, prefix("r%d" % n,"e2")))

        '''if faces is not False:
            # If faces is False, then we have connected tabedge and slotedge with a tab
            self.addInterface("tabedge", EdgePort(self, fromEdge))
            self.addInterface("slotedge", EdgePort(self, prefix("r%d" % (faces or range(4))[0],"e3")))'''


if __name__ == "__main__":
    b = RectBeam()
    # b._make_test()
