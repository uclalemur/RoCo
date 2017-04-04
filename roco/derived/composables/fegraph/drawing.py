"""Drawing module

This module contains the Drawing class, a class meant to represent unfolded
components in 2D form, and several geometric helper functions to aid in the
creation of Drawings from Graphs.
"""
def diff_edge(pts1, pts2, dimension, tolerance = 0.01):
    """Determines if two edges are the same
    """
    if tolerance < 0:
        tolerance = -tolerance
    for i in range(2):
        for j in range(dimension):
            diff1 = pts1[i][j] - pts2[i][j]
            diff2 = pts1[1-i][j] - pts2[i][j]
            if (tolerance < diff1 or diff1 < -tolerance) and (tolerance < diff2 or diff2 < -tolerance): #Allow for some difference due to double precision
            return True
    return False

def update_dimensions(dimensions, point):
    """Updates the max x and y of dimension

    Args:
        dimensions (list): The current max x and y
        point (list): the x and y of the point

    Returns:
        The new dimensions list
    """
    if dimensions[0][0] is None:
        return [[point[0],point[1]],[point[0],point[1]]]
    if point[0] < dimensions[0][0]:
        dimensions[0][0] = point[0]
    if point[1] < dimensions[0][1]:
        dimensions[0][1] = point[1]
    if point[0] > dimensions[1][0]:
        dimensions[1][0] = point[0]
    if point[1] > dimensions[1][1]:
        dimensions[1][1] = point[1]
    return dimensions

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

    def __init__(self):
        """
        Initializes an empty dictionary to contain Edge instances.
        Keys will be Edge labels as strings. Key values will be Edge instances.
        """
        self.edges = {}
        self.faces = []
        self.dimensions = [[None, None], [None, None]]

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
        self.place_face(g.faces[0], None, np.eye(4), np.eye(4))
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
        try:
            vertex_coordinates[0][0]
        except TypeError:
            vertex_coordinates = vertex_coordinates.tolist()
        vertices = []
        v1 = (round(vertex_coordinates[0][0], 3), round(vertex_coordinates[1][0], 3))
        for i in range(len(vertex_coordinates[0])):
            # print vertex_coordinates[0][i],vertex_coordinates[1][i],"-----"
            vertex = (round(vertex_coordinates[0][i], 3), round(vertex_coordinates[1][i], 3))
            self.dimensions = update_dimensions(self.dimensions, vertex)
            vertices.append(vertex)
        vertices.append(v1)
        face = geometry.Polygon(vertices)
        # print len(self.faces)
        if allow_overlap:
            for f in self.faces:
                if face.crosses(f):  # or face.within(f) or face.contains(f) or f.equals(f):
                    # print "cross", list(face.exterior.coords), list(f.exterior.coords)
                    return False
                if face.within(f):
                    # print "within", list(face.exterior.coords), list(f.exterior.coords)
                    return False
                if face.contains(f):
                    # print "contains", list(face.exterior.coords), list(f.exterior.coords)
                    return False
                if face.equals((f)):
                    # print "equals", list(face.exterior.coords), list(f.exterior.coords)
                    return False
                if face.overlaps(f):
                    return False

        self.faces.append(face)
        return True

    def place_face(self, face, edge_from, edge_from_pts, transform2D, placed=None):
        """Probably needs to be completely rewritten
        """
        checkForOverlap = False
        if placed is not None and face in placed['faces']:
            # TODO : verify that it connects appropriately along alternate path
            # print "Repeated face : " + self.name
            return
        if placed is None:  # Replacing the entire component
            placed = {'faces': [], 'edges': {}, 'overlapping': []}
            checkForOverlap = True

        for e in face.get2DDecorations():
            self.edges[e[0]] = Edge(e[0], [self.component.evalEquation(x) for x in e[1]],
                                    [self.component.evalEquation(x) for x in e[2]], EdgeType(e[3]))

        if edge_from is not None:
            r = face.preTransform(edge_from)  # Get Rotation angle of previous edge
        else:
            r = np.eye(4)  # Place edge as is

        # Rotate face to new direction
        facetransform2D = np.dot(transform2D, r)

        pts2d = np.dot(r, face.pts4d)[0:2, :]

        # print self.component.evalEquation(np.dot(facetransform2D, face.pts4d))
        pts2dMatrix = np.dot(r, face.pts4d)
        coords2DMatrix = np.dot(facetransform2D, face.pts4d)

        coords2D = np.dot(facetransform2D, face.pts4d)[0:2, :]

        facepts2d = []
        faceedges = []
        coords2D = self.component.evalEquation(coords2D)
        # print coords2D
        # print self.component.evalEquation(pts2d), self.component.evalEquation(face.pts4d), self.component.evalEquation(coords2D)
        for (i, e) in enumerate(face.edges):
            if e is None:
                continue

            if e.name[:4] == 'temp':
                continue

            try:
                da = e.faces[face]
            except KeyError:
                # Edge was added as a cut
                continue
            facepts2d.append((coords2D[:, i - 1], coords2D[:, i]))
            faceedges.append(e)
            '''if da[1]:
              facepts2d.append((coords2D[:, i - 1], coords2D[:, i]))
            else:
              facepts2d.append((coords2D[:, i], coords2D[:, i - 1]))
          if not self.placeFace(faceedges,facepts2d):
            raise Exception("Attemping to place overlapping faces")'''

        if not self.placeFace(faceedges, facepts2d, coords2D):
            try:
                edge_from = self.component.evalEquation(edge_from)
            except:
                pass

            reflection = ReflectAcross2Dpts(edge_from_pts)
            reflectionX = np.array([[1, 0, 0, 0],
                                    [0, -1, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]])

            if edge_from is not None:
                r = face.preTransform(edge_from)  # Get Rotation angle of previous edge
            else:
                r = np.eye(4)  # Place edge as is
            r = np.dot(reflectionX, r)

            pts2d = np.dot(r, face.pts4d)[0:2, :]
            # print self.component.evalEquation(reflection)
            coords2D = np.dot(reflection, coords2DMatrix)[0:2, :]
            # print self.component.evalEquation(pts2d), self.component.evalEquation(face.pts4d), self.component.evalEquation(coords2D)

            facepts2d = []
            faceedges = []
            coords2D = self.component.evalEquation(coords2D)

            # print coords2D
            for (i, e) in enumerate(face.edges):
                if e is None:
                    continue

                if e.name[:4] == 'temp':
                    continue

                try:
                    da = e.faces[face]
                except KeyError:
                    # Edge was added as a cut
                    continue
                facepts2d.append((coords2D[:, i - 1], coords2D[:, i]))
                faceedges.append(e)
            if not self.placeFace(faceedges, facepts2d, coords2D):
                placed['overlapping'].append(face)
                return

        # Face is being placed
        placed['faces'].append(face)
        if face in placed['overlapping']:
            placed['overlapping'].remove(face)

        for i in range(len(faceedges)):
            # Don't 2d place edges that are tabbed
            e = faceedges[i]
            if e.isTab():
                edgepts2d = None
            # Evaluate the edge coordinates
            edgepts2d = (self.component.evalEquation(facepts2d[i][0]), self.component.evalEquation(facepts2d[i][1]))

            '''for ple in placed['edges'].keys():
              if intersects(edgepts2d,placed['edges'][ple]):
                print 'Error: Edge Intersects', edgepts2d, placed['edges'][ple]
                continue'''
            # Deal with edges that are connected in 3D, but not in 2D
            if e.name in placed['edges'].keys() and diffEdge(placed['edges'][e.name], edgepts2d,
                                                             2):  # If edges has already been placed, it must be cut
                # Create a new edge
                self.edges['temp' + e.name] = Edge('temp' + e.name, edgepts2d[0], edgepts2d[1], Cut())
                # Make old edge into a cut
                self.edges[e.name] = Edge(e.name, placed['edges'][e.name][0], placed['edges'][e.name][1], Cut())

            else:
                if len(e.faces) == 1:
                    edge = Cut()
                else:
                    edge = Fold()
                self.edges[e.name] = Edge(e.name, edgepts2d[0], edgepts2d[1], edge)
                placed['edges'][e.name] = edgepts2d

            if len(e.faces) <= 1:
                # No other faces to be found, move on to next edge.
                continue
            if e.isTab():
                # Don't follow faces off of a Tab
                continue

            # XXX hack: don't follow small edges
            el = face.edgeLength(i)
            try:
                if el <= 0.01:
                    continue
            except TypeError:
                pass  # print 'sympyicized variable detected - ignoring edge length check'

            pt1 = pts2d[:, i - 1]
            pt2 = pts2d[:, i]

            # TODO : Only skip self and the face that you came from to verify multi-connected edges
            # XXX : Assumes both faces have opposite edge orientation
            #       Only works for non-hyper edges -- need to store edge orientation info for a +/- da
            for (f, a) in e.faces.iteritems():
                '''if a[1] ^ da[1]:
                  # opposite orientation
                  pta, ptb = pt1, pt2
                else:
                  # same orientation'''
                pta, ptb = pt1, pt2
                x = RotateXTo(ptb, pta)

                r2d = np.eye(4)
                r2d = np.dot(x, r2d)
                r2d = np.dot(MoveOriginTo(pta), r2d)

                self.place(f, e, edgepts2d, np.dot(transform2D, r2d), placed)
        if checkForOverlap and len(placed['overlapping']):
            raise Exception('One or more faces could not be placed without overlap!')

    def to_DXF(self, filename=None, labels=False, mode="dxf"):
        """
        """
        from dxfwrite import DXFEngine as dxf
        dwg = dxf.drawing(filename)
        EdgeType.makeLinetypes(dwg, dxf)
        for e in self.edges.items():
            e[1].toDrawing(dwg, e[0] if labels else "", mode=mode, engine=dxf)
        dwg.save()

    def to_SVG(self, filename, labels=False, mode=None, save_to_file=True):
        """
        """
        import svgwrite

        dim = self.getDimensions()
        w = int(dim[1][0] - dim[0][0])
        h = int(dim[1][1] - dim[0][1])
        size = ('{}mm'.format(w), '{}mm'.format(h))

        printSVG = svgwrite.Drawing(filename, size=size, viewBox=('0 0 {} {}'.format(w, h)))
        viewSVG = svgwrite.Drawing("view" + filename, viewBox=('0 0 {} {}'.format(w, h)))
        for e in self.edges.items():
            e[1].toDrawing(printSVG, e[0] if labels else "", mode)
            e[1].toDrawing(viewSVG, e[0] if labels else "", mode)
        if save_to_file:
            printSVG.save()
            # viewSVG.save()
        else:
            return (printSVG.tostring(), viewSVG.tostring())

    def get_dimensions(self):
        """Gets the maximum dimensions of the current drawing

        Args:
            None

        Returns:
            A 2D array representation of the bounding box of the Drawing in the
            form [[xmin,ymin],[xmax,ymax]].
        """
        return self.dimensions

    def rename_edge(self, old_name, new_name):
        """Renames an edge in the drawing

        Args:
            old_name (str): the name of the edge to be renamed
            new_name (str): the new name of the edge

        Returns:
            The current drawing.
        """
        self.edges[toname] = self.edges.pop(fromname)
        self.edges[toname].name = toname

        return self

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
        if relative is not None:
            pts = [x[0] for x in self.edgeCoords()] + [x[1] for x in self.edgeCoords()]
            xs = [x[0] for x in pts]
            ys = [x[1] for x in pts]
            minx = min(xs)
            maxx = max(xs)
            miny = min(ys)
            maxy = max(ys)
            midx = minx + relative[0] * (maxx + minx)
            midy = miny + relative[1] * (maxy + miny)
            origin = (origin[0] - midx, origin[1] - midy)

        for e in self.edges.values():
            e.transform(scale=scale, angle=angle, origin=origin)

        return self


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
        for e in dwg.edges.items():
            self.edges[prefix_string(prefix, e[0])] = e[1].copy()
            self.edges[prefix_string(prefix, e[0])].transform(**kwargs)
        return self

    def copy(self, prefix = ''):
        """Creates a copy of the current drawing

        Args:
            prefix (str): a prefix string to be prepended to all edges in the
                drawing copy

        Returns:
            A Drawing object that is a copy of the current drawing
        """
        c = Drawing()
        for e in self.edges.items():
            c.edges[prefix_string(prefix, e[0])] = e[1].copy()
        return c
