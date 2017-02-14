"""Drawing module

This module contains the Drawing class, a class meant to represent unfolded
components in 2D form, and several geometric helper functions to aid in the
creation of Drawings from Graphs.
"""

class Drawing():
    """A 2D representation of unfolded components.

    A Drawing is a collection of Drawingedges and faces which represent
    the unfolded 2D version of a component. Drawings can be created from
    Graphs, and can be output to SVG or DXF formats

    Attributes:
        edges (dict): a dictionary of DrawingEdges that make up the drawing
        faces (list): DEPRECATED?
        dimenstions (list): a 2D array representation of the bounding
            box of the Drawing in the form [[xmin,ymin],[xmax,ymax]]
        component (FoldedComponent): a reference to the component
            represented by the Drawing

    """

    def from_graph(self, graph, component=None):
        """Creates a 2D representation of the input graph and adds it to the
        current drawing.

        Args:
            graph (FaceEdgeGraph): the face edge graph from which to create
                a drawing
            component (FoldedComponent): the FoldedComponent associated with the
                graph and drawing, used to compute the literal values for
                symbolic coordinates
        """
    def add_face(self, vertex_coordinates, allow_overlap=False):
        """Adds a face whose boundary is defined by the vertices in
        vertex_coordinates using right handed convention. If allow_overlap is
        not True, the face will not be placed if it overlaps a previous placed
        face.

        Args:
            vertex_coordinates (Matrix/List): a 2D list of the x and y
                coordinates of each vertex. Vertices should be ordered according
                to a right handed convention, i.e. counter-clockwise around the
                area of the face.
            allow_overlap (bool): if False, the face will only be placed if its
                area does not overlap with the area of a previously placed face.
                If True, any face with valid coordinates will be added to the
                drawing.
        Returns:
            True if the face was placed correctly, False if the face causes
            overlap when not allowed.
        """
    def place_face(self, face, edge_from, edge_from_pts, transform_2D, placed=None):
        """
        """
    def to_DXF(self, filename=None, labels=False, mode="dxf"):
        """
        """
    def to_SVG(self, filename, labels=False, mode=None, save_to_file=True):
        """
        """
    def get_dimensions(self):
        """Gets the maximum dimensions of the current drawing

        Args:
            None

        Returns:
            A 2D array representation of the bounding box of the Drawing in the
            form [[xmin,ymin],[xmax,ymax]].
        """
    def rename_edge(self, old_name, new_name):
        """Renames an edge in the drawing

        Args:
            old_name (str): the name of the edge to be renamed
            new_name (str): the new name of the edge

        Returns:
            The current drawing.
        """
    def transform(self, scale=1, angle=0, origin=(0,0), relative=None):
        """Rotates and scales the drawing according to the specified arguments

        Args:
            scale (float): the factor by which the drawing will be scaled
            angle (float): the angle in radians by which the drawing will be
                rotated
            origin (tuple): the point around which to rotate and scale the
                drawing
            relative (tuple): if not None, the origin is taken to be an offset
                from this relative position in the drawing

        Returns:
            The transformed Drawing.
        """
    def append_drawing(self, drawing, prefix = '', **kwargs):
        """Appends edges from another drawing to the current drawing

        Args:
            drawing (Drawing): the drawing whose edges will be added to the
                current drawing
            prefix (str): a prefix string to be prepended to all newly added
                edge names
            **kwargs: optional arguments specifying a transformation to be
                applied to added edges

        Returns:
            The Drawing with the added edges.
        """
    def copy(self, prefix = ''):
        """Creates a copy of the current drawing

        Args:
            prefix (str): a prefix string to be prepended to all edges in the
                drawing copy

        Returns:
            A Drawing object that is a copy of the current drawing
        """
