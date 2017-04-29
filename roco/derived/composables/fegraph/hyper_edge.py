class HyperEdge():
    """HyperEdge represents the connection between two or more Face objects

    Attributes:
        name (str): A name for the edge
        length (int): The length of the edge
        tab_width (???): ???
        pts_2D (???): ???
        pts_3D (???): ???
        edge_type (str): Either "FOLD", "BEND", or "JOINT", represents
            the type of edge
        joints (list): ???
        faces (dict): A dictionary of the faces attached to the edge

    """

    #ANDYTODO: transform these into sublclasses of HyperEdge and/or componenet
    edge_types = ["FOLD", "BEND", "JOINT"]

    @staticmethod
    def edge(all_edges, name, length, face, angle=0, flip=False):
        if all_edges is not None:
            for e in all_edges:
                if e.name == name:
                  e.join(length, face=face, angle=angle, flip=flip)
                  return e
        e = HyperEdge(name, length, face, angle, flip)
        try:
            allEdges.append(e)
        except:
            pass
        return e

    def __init__(self, name, length, face=None, angle=0, flip=False):
        self.name = name
        self.length = length
        self.tab_width = None
        self.pts_2D = None
        self.pts_3D = None
        self.edge_type = "FOLD"
        self.joints = []
        if face:
            self.faces = {face: (angle, flip)}
        else:
            self.faces = {}

    def update_subs(self, subs):
        if isinstance(self.length, math.Symbol):
            self.length = self.length.subs(subs)
        if self.pts_2D is not None and len(self.pts_2D) == 2 and len(self.pts_2D[0]) == 2:
            self.pts_2D = tuple(sympy.ImmutableMatrix([dim.subs(subs) if isinstance(dim, sympy.Basic) else dim for dim in p]) for p in self.pts_2D)
        if self.pts_3D is not None and len(self.pts_3D) == 2 and len(self.pts_3D[0]) == 3:
            self.pts_3D = tuple(sympy.ImmutableMatrix([dim.subs(subs) if isinstance(dim, sympy.Basic) else dim for dim in p]) for p in self.pts_3D)

    def remove(self, face):
        """Remove a face associated with the edge

        Args:
            face: The face to be removed
        """
        if face in self.faces:
            self.faces.pop(face)
        try:
            face.disconnect_from(self.name)
        except (ValueError, AttributeError):
            pass

    def rename(self, name):
        """Rename the edge

        Args:
            name: the new name for the edge
        """

        self.name = name

    def is_tab(self):
        """Returns True if the edge is a tab

        Args:
            None

        Returns:
            True if the edge is a tab, False otherwise
        """
        return self.tab_width is not None

    def set_angle(self, face, angle, flip=False):
        """Set the angle of a face relative to the edge

        Args:
            face: the face whose angle is being set
            angle: the angle of the face
            flip: whether or not to flip the face relative to the edge
        """
        if face in self.faces:
            self.faces[face] = (angle, flip)

    def get_interior_angle(self):
        """Returns the angle between faces associated with edge

        Args:
            None

        Returns:
            None if the edge only has one face, the angle between two associated
                faces if there are two, and a ValueError otherwise
        Raises:
            ValueError: The edge has more than two associated faces
        """

        if len(self.faces) == 1:
            return None
        elif len(self.faces) == 2:
            angles = self.faces.values()
            if angles[0][1]:
                return angles[0][0] - angles[1][0]
            else:
                return angles[1][0] - angles[0][0]
        else:
            raise ValueError("Don't know how to handle edge with %d faces" % len(self.faces))

    def flip_connection(self, face):
        """Flips the connection of the given face

        Args:
            face: the face to be flipped
        """
        if face in self.faces:
            oldangle = self.faces[face]
            self.faces[face] = (oldangle[0], not oldangle[1])

    def join(self, length, face, from_face=None, angle = 0, flip = True):
        """Join a new face to the edge

        Args:
            length: the length of the face
            face: the face to be joined
            from_face: the face to join relative to
            angle: the angle to join at
            flip: if true, the face will be flipped
        """
        if not self.matches_length(length):
            raise ValueError("Face %s of length %f cannot join edge %s of length %f." % (face.name, length, self.name, self.length))
        baseangle = 0
        if from_face in self.faces:
            baseangle = self.faces[from_face][0]
        newangle = (baseangle+angle) % 360
        self.faces[face] = (newangle, flip)

    TOL = 5e-2
    def matches_length(self, length, tolerance=self.TOL):
        """Check if a length is the same as the length of the edge, within a
            tolerance

        Args:
            length: the length to check
            tolerance: the tolerance to check to

        Returns:
            True if the edges are the same within the tolerance or symbolic, and
                False otherwise
        """
        try:
            # XXX: Hack to force type error testing here
            if np.simplify(self.length - length) < tolerance:
                return True
            else:
                return False
        except TypeError:
        #print 'Sympyicized variable detected in matches_length, ignoring for now, returning true'
        #print self.length, length
            return True

    def merge_with(self, other, angle=0, flip=False, tab_width=None):
        """Combine two separate edges into one. All faces associated with the
            two edges will be connected to the new edge

        Args:
            other: the edge to be merged with
            angle: the angle to merge the edges at
            flip: whether to flip the edge when merging
            tab_with: the width of the tab associated with the edge
        """
        # Takes all of the faces in other into self
        if other is None:
            return self
        self.tab_width = tab_width
        other.tab_width = tab_width

        if not self.matches_length(other.length):
            raise ValueError("Edge %s of length %f cannot merge with edge %s of length %f." %
                            (other.name, other.length, self.name, self.length))

        for face in other.faces.keys():
            oldangle = other.faces[face]
            face.replace_edge(other, self, angle = (angle+oldangle[0]), flip = (flip ^ oldangle[1]))
        return self

    def place(self, pts_2D, pts_3D):
        """Set the 2D and 3D position of the edge

        Args:
            pts_2D: the 2D pts of the edge
            pts_3D the 3D pts of the edge
        """
        self.pts_2D = pts_2D
        self.pts_3D = pts_3D

    def get_3D_COM(self):
        """Get the 3D center of mass of the object.

        Args:
            None

        Returns:
            The 3D center of mass of the object
        """
        return (self.pts_3D[0] + self.pts_3D[1])/2

    def set_type(self, edge_type):
        """Set the edge type of the edge

        Args:
            edge_type: the new edge_type for the edge

        Raises:
            Exception: the given edge_type does not exist
        """
        if edge_type is None:
            return # do nothing
        if edge_type not in self.edge_types:
            raise Exception("Invalid edge type!")
        self.edge_type = edge_type

    def add_joint(self, joint):
        """Add a new join to the edge

        Args:
            joint: the joint being added

        Raises:
            Exception: the edge is not a joint edge
            Exception: joint is not a Joint object
        """
        if not self.edge_type is "JOINT":
            raise Exception("Trying to add joints to a non-joint edge")
        if not isinstance(joint, Joint):
            raise Exception("Not a joint!")
        self.joints.append(joint)

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name + ": " + repr(self.faces)

    def __repr__(self):
        # return self.name + " [ # faces : %d, len : %d ]" % (len(self.faces), self.length)
        ret = "%s#%d" % (self.name, len(self.faces))
        if len(self.faces) > 1:
        return ret + repr(self.faces.values())
        else:
        return ret
