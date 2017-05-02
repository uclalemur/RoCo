"""Drawing module

This module contains the Drawing class, a class meant to represent unfolded
components in 2D form, and several geometric helper functions to aid in the
creation of Drawings from Graphs.
"""

import roco.utils.mymath as np
from roco.api.utils.variable import eval_equation
from drawing_edge import *
from roco.utils.transforms import *
from shapely import geometry

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
        self.place_faces(graph.faces[0], None, np.eye(4))
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

    def place_faces(self, face, edge_from, transform_2D, placed=None, allow_overlap=False):
        """Recursively adds faces to the 2D drawing.

        Args:
            face: the current face being placed
            edge_from: the edge by which to attach the current face
            transform_2D: A tranformation matrix to move the face into its position in 2D space
            placed: dictionary containing metadata about previously placed entities
            allow_overlap: Whether or not to allow two face to be placed on top of each other
        """

        if placed is not None and face in placed['faces']:
            #This face has already been placed, do not place again
            return

        if placed is None:
            #No faces have been placed yet, initialize data structures
            placed = {'faces': [], 'edges': {}, 'overlapping': []}
            check_for_overlap = not allow_overlap
        else:
            #Overlap checking is handled only in top level call
            check_for_overlap = False

        #Will this break if a face has to be flipped?
        for e in face.get_2D_decorations():
                self.edges[e[0]] = Edge(e[0], [eval_equation(x) for x in e[1]],
                                        [eval_equation(x) for x in e[2]], EdgeType(e[3]))

        """
        Placing faces involves the notion of "pretransformed" and "transformed" values.
        Pretransformation moves the edge a face is being connected by to the x axis,
        and can be thought of as a face's relative position to its neighbor.
        Transformation moves a face to its absolute position in 2D space.
        """
        if edge_from is not None:
            #Align connected edges
            pretransform_matrix = face.pre_transform(edge_from)
        else:
            #Place edge as is
            pretransform_matrix = np.eye(4)

        transform_matrix = np.dot(transform_2D, pretransform_matrix)

        #4D pts are the homogenous coordinates of the face i.e. [x,y,z,1]
        pretransformed_pts_4D = np.dot(pretransform_matrix, face.pts_4D)
        transfromed_pts_4D = np.dot(transform_matrix, face.pts_4D)

        pretransformed_pts_2D = pretransformed_pts_4D[0:2,:]
        #Numerical values for the coordinates are required for placement
        transfromed_pts_2D = eval_equation(transfromed_pts_4D[0:2, :])

        if not self.add_face(transfromed_pts_2D):
            #If face cannot be placed without collisions, attempt to reflect it
            reflection_matrix = np.array([[1,  0, 0, 0],
                                          [0, -1, 0, 0],
                                          [0,  0, 1, 0],
                                          [0,  0, 0, 1]])

            #Recompute pretransform and transform with rotation
            pretransform_matrix = np.dot(reflection_matrix, pretransform_matrix)
            transform_matrix = np.dot(transform_2D, pretransform_matrix)

            pretransformed_pts_4D = np.dot(pretransform_matrix, face.pts_4D)
            transfromed_pts_4D = np.dot(transform_matrix, face.pts_4D)

            pretransformed_pts_2D = pretransformed_pts_4D[0:2,:]
            transfromed_pts_2D = eval_equation(transfromed_pts_4D[0:2, :])

            if not self.add_face(transfromed_pts_2D) and not allow_overlap:
                #Face was not able to be placed connected to this edge
                #Keep track of face and hope it gets placed elsewhere
                #TODO: Try connecting along other edges or undoing previous placements?
                placed['overlapping'].append(face)
                return
        #Face is being placed
        placed['faces'].append(face)
        if face in placed['overlapping']:
            placed['overlapping'].remove(face)

        #Place each edge
        for (i, edge) in enumerate(face.edges):
            #HACK: Do not place temporary edges
            if edge is None or edge.name[:4] == "temp":
                continue

            #Get the endpoints of the edge
            edge_pts_2D = (transfromed_pts_2D[:,i - 1],transfromed_pts_2D[:,i])

            if edge.name in placed['edges'].keys():
                edge_alias = placed['edges'][edge.name]
                if diff_edge(edge_alias, edge_pts_2D,2):
                #If the edge has already been placed in a different place, a cut must be made

                #Create a new edge
                    self.edges['temp' + edge.name] = DrawingEdge('temp' + edge.name, edge_pts_2D[0], edge_pts_2D[1], Cut())
                # Make old edge into a cut
                self.edges[edge.name] = DrawingEdge(edge.name, edge_alias[0], edge_alias[1], Cut())
            else:
                #Add edge normally
                if len(edge.faces) == 1:
                    edge_type = Cut()
                else:
                    edge_type = Fold()
                self.edges[edge.name] = DrawingEdge(edge.name, edge_pts_2D[0], edge_pts_2D[1], edge_type)
                placed['edges'][edge.name] = edge_pts_2D

            if len(edge.faces) <= 1:
                # No other faces to be found, move on to next edge.
                continue
            if edge.is_tab():
                # Don't follow faces off of a Tab
                continue

            #Compute new transform matrix for next face
            rotation_matrix = rotate_x_to(pretransformed_pts_2D[:,i],pretransformed_pts_2D[:,i-1])
            origin_matrix = move_origin_to(pretransformed_pts_2D[:,i-1])
            next_transfrom_2D = np.dot(transform_2D,np.dot(origin_matrix,np.dot(rotation_matrix,np.eye(4))))

            #Place faces connected to edge
            for(f,a) in edge.faces.iteritems():
                self.place_faces(f, edge, next_transfrom_2D, placed)
        if check_for_overlap and len(placed['overlapping']):
            #Placement has finished, but some edges are still unplaced
            raise Exception('One or more faces could not be placed without overlap!')

    def to_DXF(self, filename=None, labels=False, mode="dxf"):
        """
        """
        from dxfwrite import DXFEngine as dxf
        dwg = dxf.drawing(filename)
        EdgeType.make_linetypes(dwg, dxf)
        for e in self.edges.items():
            e[1].to_drawing(dwg, e[0] if labels else "", mode=mode, engine=dxf)
        dwg.save()

    def to_SVG(self, filename, labels=False, mode=None, save_to_file=True):
        """
        """
        import svgwrite

        dim = self.get_dimensions()
        w = int(dim[1][0] - dim[0][0])
        h = int(dim[1][1] - dim[0][1])
        size = ('{}mm'.format(w), '{}mm'.format(h))

        printSVG = svgwrite.Drawing(filename, size=size, viewBox=('0 0 {} {}'.format(w, h)))
        viewSVG = svgwrite.Drawing("view" + filename, viewBox=('0 0 {} {}'.format(w, h)))
        for e in self.edges.items():
            e[1].to_drawing(printSVG, e[0] if labels else "", mode)
            e[1].to_drawing(viewSVG, e[0] if labels else "", mode)
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

    def edge_coords(self):
        """ Returns a list of all edge coordinates
        
        Returns:
            a list of all Edge instance endpoints in Drawing

        """
        edges = []
        for e in self.edges.items():
            edges.append(e[1].coords())
        return edges

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
            pts = [x[0] for x in self.edge_coords()] + [x[1] for x in self.edge_coords()]
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

class Face(Drawing):
  def __init__(self, pts, edgetype = None, origin = True):
    Drawing.__init__(self)
    if origin:
      pts = list(pts) + [(0,0)]
    else:
      pts = list(pts)

    lastpt = pts[-1]
    edgenum = 0
    edgenames = []
    for pt in pts:
      name = 'e%d' % edgenum
      self.edges[name] = Edge(name, lastpt, pt, edgetype)
      edgenames.append(name)
      lastpt = pt
      edgenum += 1

class Rectangle(Face):
  def __init__(self, l, w, edgetype = None, origin = True):
    Face.__init__(self, ((l, 0), (l, w), (0, w), (0,0)), edgetype, origin)
