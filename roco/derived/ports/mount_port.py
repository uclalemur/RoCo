from roco.api.port import Port
"""MountPort class.

This module contains the MountPort class.

"""

class MountPort(Port):
    """A class representing the connection between a physical object and a
    mechanical face. MountPorts contain decorations, which are cutouts that
    allow for phycial objects to be placed onto faces

    Attributes:
        decoration (Decoration): A graph containing the face holes for the mount

    """
    def __init__(self, parent, decoration):
        Port.__init__(self, parent, {})
        self.decoration = decoration

    def get_decoration(self):
        return self.decoration

    def toString(self):
        print "decoration"

    def can_mate(self, other_port):
        try:
            return (other_port.get_face_name() is not None)
        except AttributeError:
            return False

if __name__ == "__main__":
    pass
    