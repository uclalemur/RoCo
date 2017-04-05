"""FacePort class.

This module contains the FacePort class.

"""

from six_dof_port import SixDOFPort

class FacePort(SixDOFPort):
    """A class representing a physical face that can be connected to.

    Attributes:
        face (Face): holds the Face object on the parent graph that this port
        is associated with.

    """
    def __init__(self, parent, face):
        """Creates a edge port object.

        Args:
            parent (component): The component to which this port will be added.
            face: the face associated with the port
        """
        self.face = parent.get_graph().get_face(face)
        SixDOFPort.__init__(self, parent, self.face)

    def get_face_name(self):
        """Returns the name of the associated face

        Args:
            None

        Returns:
            The name of the face
        """
        return self.face.name

    def get_points(self):
        """Returns the points associated with the face

        Args:
            None

        Returns:
            Face points
        """
        pts = self.face.get_3D_coords()
        return [pts[:, x] for x in range(len(pts[0, :]))]

    def __str__(self):
        return str(self.face.name)

    def can_mate(self, other_port):
        """Returns true if this port can mate with other_port and false otherwise.

        Args:
            other_port (Port): the port that is compared to this port to check compatibility.

        Returns:
            Boolean denoting whether or not the ports are compatible.
        """
        try:
            return (otherPort.get_decoration() is not None)
        except AttributeError:
            return False
