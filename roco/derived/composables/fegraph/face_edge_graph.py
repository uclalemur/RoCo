"""
Contains the Graph class and several helper functions.
"""

from roco.derived.composables.fegraph.hyper_edge import HyperEdge
from roco.utils import mymath as np
from roco.utils.utils import prefix as prefix_string
import copy

def inflate(face, thickness=.1, edges=False):
    """
    Inflates a face by creating two faces that are thickness apart.

    Args:
        face (Face): the Face object to inflate.
        thickness (float): the thickness to create the inflated face with.
        edges (bool): whether to return faces as a list of edges or as Face objects.

    Returns:
        List of two new faces that represent the inflated face.

    """
    dt = np.array([[0],[0],[thickness/2.],[0]])
    nf = face-dt
    pf = face+dt

    faces = []

    if edges:
      faces.append(np.transpose(np.array((pf[:,0], nf[:,0], pf[:,1]))))
      faces.append(np.transpose(np.array((nf[:,0], nf[:,1], pf[:,1]))))
    else:
      faces.append(pf)          # top face
      faces.append(nf[:,::-1])  # bottom face

    return faces

def stl_write(faces, filename, thickness=0):
    """
    Writes a graph object represented by faces to an STL file.
    
    Args:
        faces (list): list of faces that compose the object.
        filename (str): filename to write STL to.
        thickness (int or float): thickness of each face to draw.
    
    """
    import triangle

    shape = None
    shells = []
    triangles = []
    for f in faces:
      r = f[0]
      A = f[1]

      facets = []
      B = triangle.triangulate(A, opts='p')
      if not 'triangles' in B:
        print "No triangles in " + f[2]
        continue

      if thickness:
        for t in [np.transpose(np.array([list(B['vertices'][x]) + [0,1] for x in (face[0], face[1], face[2])])) for face in B['triangles']]:
          facets.extend([np.dot(r, x) for x in inflate(t, thickness=thickness)])
        for t in [np.transpose(np.array([list(A['vertices'][x]) + [0,1] for x in (edge[0], edge[1])])) for edge in A['segments']]:
          facets.extend([np.dot(r, x) for x in inflate(t, thickness=thickness, edges=True)])
      else:
        for t in [np.transpose(np.array([list(B['vertices'][x]) + [0,1] for x in (face[0], face[1], face[2])])) for face in B['triangles']]:
          facets.append(np.dot(r, t))

      triangles.extend(facets)

      if thickness:
        FREECADPATH = '/usr/lib64/freecad/lib'
        import sys
        sys.path.append(FREECADPATH)
        import Part
        meshes = []
        for f in (np.transpose(t[0:3,:]) for t in facets):
          try:
            meshes.append(Part.Face(Part.Wire([Part.makeLine(tuple(f[x]), tuple(f[x-1])) for x in range(3)])))
          except RuntimeError:
            print "Skipping face: " + repr(f)
        shell = Part.makeShell(meshes)
        shells.append(shell)
        if shape is None:
          shape = shell
        else:
          shape = shape.fuse(shell)

    if shape:
      with open("freecad" + filename, 'wb') as fp:
        shape.exportStl("freecad" + filename)

    from stlwriter import Binary_STL_Writer
    faces = triangles

    with open(filename, 'wb') as fp:
      writer = Binary_STL_Writer(fp)
      writer.add_faces(faces)
      writer.close()

def dxf_write(edges, filename):
    """
    Writes a set of edges to a DXF file.

    Args:
        edges (Iterable): collection of edges to write
        filename (str): name of the DXF file to write to

    """
    from dxfwrite import DXFEngine as dxf
    dwg = dxf.drawing(filename)
    for e in edges:
      if e[2] is None:
        kwargs = {"layer": "Cut"}
      else:
        kwargs = {"layer": repr(e[2])}
      dwg.add(dxf.line((e[0][0], e[0][1]), (e[1][0], e[1][1]), **kwargs))
    dwg.save()

class FaceEdgeGraph(object):
    """
    A face-edge graph consisting of Face and HyperEdge objects

    Attributes:
        edges (list): A List of HyperEdge objects that make up the edges of
            the Graph
        faces (list): A list of Face objects that make up the vertices of the
            Graph
        transform3D (Matrix): Matrix representing the position and
            transformation of the Graph in 3D spaces
    """

    def __init__(self, transform=None):
        """
        Initializes this face-edge graph object
        
        Attributes:
            transform: the initial transform of this object

        """
        self.faces = []
        self.edges = []
        self.placed = False
        self.prefixed = False
        self.transform3D = transform or np.eye(4)

    def add_face(self, f, prefix=None, face_edges=None, face_angles=None, face_flips=None):
        """
        Adds a face to this graph object

        Attributes:
            f (Face): Face object to add
            prefix (str): a string to prefix the face and edge names with
            face_edges ls,dfajioj
        """
        if prefix and not self.placed:
            f.prefix(prefix)
        if f in self.faces:
            raise ValueError("Face %s already in graph" % f.name)
        self.faces.append(f)

        if face_edges is not None:
            f.rename_edges(face_edges, face_angles, face_flips, self.edges)
        if prefix and not self.placed:
            f.prefix_edges(prefix)

        self.rebuildEdges()
        return self

    def attach_face(self, from_edge, new_face, new_edge, prefix=None, angle=0, edge_type=None, joints=None):
        """
        Attaches a face to the graph object, merging edges if necessary.

        Args:
            from_edge (HyperEdge): edge from the graph object that the new face is being connected to
            new_face (Face): the new face being attached
            new_edge (HyperEdge): the edge on the new face that is being connected to from_edge
            prefix (str): name prefix
            angle (numeric): the angle of connection between the edges
            edge_type (str): the type of edge("FOLD", "CUT", "JOINT")
            joints (list): list of joints to add to the new edge
        """
        # XXX should set angle from a face, not absolute angle of the face
        self.add_face(new_face, prefix)

        if from_edge is not None:
          new_edge = prefix_string(prefix, new_edge)
          self.merge_edge(from_edge, new_edge, angle=angle, edge_type=edge_type, joints=joints)

    def del_face(self, facename):
        """
        Deletes a face from the graph object

        Args:
            facename (str): name of the face to remove

        Returns:
            the modified graph object
        """
        for (i, f) in enumerate(self.faces):
            if f.name == facename:
                f.disconnectAll()
                self.faces.pop(i)
                self.rebuildEdges()
                return self

        return self

    def get_face(self, name):
        """
        Finds and returns a Face object by name

        Args:
            name (str): the name of the Face to return

        Returns:
            the Face that is given by the name or None if it is not found
        """
        for f in self.faces:
            if f.name == name:
                return f
        return None

    def get_edge(self, name):
        """
        Finds and returns a HyperEdge object by name

        Args:
            name (str): the name of the HyperEdge to return

        Returns:
            the HyperEdge that is given by the name or None if it is not found
        """
        for e in self.edges:
            if e.name == name:
                return e
        return None

    def prefix(self, prefix):
        """
        Prefixes all edges and faces of this graph object

        Args:
            prefix (str): the string to prefix all faces and edges with
        """
        for e in self.edges:
            e.rename(prefixString(prefix, e.name))
        for f in self.faces:
            f.rename(prefixString(prefix, f.name))
        self.prefixed = True

    def rename_edge(self, fromname, toname):
        """
        Renames an edge in the graph

        Args:
            fromname (str): the name of the edge to rename
            toname (str): the name to change to
        """
        e = self.get_edge(fromname)
        if e:
            e.rename(toname)

    def rebuild_edges(self):
        """
        Rebuilds the list of edges by iterating through all the edges in each face
        """
        self.edges = []
        for f in self.faces:
            for e in f.edges:
                if e not in self.edges:
                    self.edges.append(e)

    def invert_edges(self):
        """
        Inverts all of the edges of the graph
        """
        # swap mountain and valley folds
        for e in self.edges:
            for f in e.faces:
                e.faces[f] = (-e.faces[f][0], e.faces[f][1])

    def add_tab(self, edge1, edge2, angle=0, width=10):
        """
        Adds a tab to the graph

        Args:
            edge1 (HyperEdge): first edge to join with the tab
            edge2 (HyperEdge): second edge to join with the tab
            angle (numeric): angle to attach the edges at
            width (numeric): width of the tab
        """
        self.merge_edge(edge1, edge2, angle=angle, tab_width=width)

    def merge_edge(self, edge1, edge2, angle=0, tab_width=None, edge_type=None, joints=None):
        """
        Merges two edges in the graph

        Args:
            edge1 (HyperEdge): first edge to merge
            edge2 (HyperEdge): second edge to merge
            angle (numeric): angle to merge edges at
            tab_width (numeric): the width of the tab to add if necessary
            edge_type (str): the type of edge the merged edge should be
            joints (list): a list of joints to add to the merged edge
        """
        e1 = self.get_edge(edge1)
        e2 = self.get_edge(edge2)
        if e1 is None:
          raise AttributeError("Edge not found: " + edge1)
        if e2 is None:
          raise AttributeError("Edge not found: " + edge2)

        if len(e2.faces) > 1:
          #print "Adding third edge"
          e2.merge_with(e1, angle=angle, flip=False, tab_width=tab_width)
        else:
          e2.merge_with(e1, angle=angle, flip=True, tab_width=tab_width)
        self.edges.remove(e1)

        e2.set_type(edge_type)
        if joints:
            for joint in joints.joints:
                e2.add_joint(joint)

        return self

    def split_edge(self, edge):
        """
        Splits an edge into two

        Args:
            edge (str): name of edge to split

        Returns:
            list of new edges and associated faces
        """
        old_edge = edge
        old_edge_name = edge.name
        new_edges_and_faces = []

        for i, face in enumerate(list(old_edge.faces)):
            length = old_edge.length
            angle = old_edge.faces[face][0]
            flip = old_edge.faces[face][1]

            new_edge_name = old_edge_name + '.se' + str(i)
            new_edge = HyperEdge(new_edge_name, length)
            face.replace_edge(old_edge, new_edge, angle, flip=False )
            new_edges_and_faces.append((new_edge_name, face, length, angle, flip))

        self.rebuild_edges()
        return new_edges_and_faces

    def tabify(self, tab_face=None, tab_decoration=None, slot_face=None, slot_decoration=None):
        """
        Adds tab and slot decorations for all edges that are tabs

        Args:
            tab_face: Face subclass that will be used for the tabs
            tab_decoration: Decoration subclass that will be used for the tabs
            slot_face: Face subclass that will be used for the slots
            slot_decoration: Decoration subclass that will be used for the slots
        """
        for e in self.edges:
          if e.is_tab():
            #print "tabbing ", e.name
            for (edgename, face, length, angle, flip) in self.split_edge(e):
              if flip:
                #print "-- tab on: ", edgename, face.name
                if tab_face is not None:
                  self.attach_face(edgename, tab_face(length, e.tab_width), "tabedge", prefix=edgename, angle=0)
                if tab_decoration is not None:
                  tab_decoration(face, edgename, e.tab_width)
              else:
                #print "-- slot on: ", edgename, face.name
                if slot_face is not None:
                  # XXX TODO: set angle appropriately
                  self.attach_face(edgename, slot_face(length, e.tab_width), "slotedge", prefix=edgename, angle=0)
                if slot_decoration is not None:
                  slot_decoration(face, edgename, e.tab_width)

        #TODO: extend this to three+ edges
        #component.addConnectors((conn, cname), new_edges[0], new_edges[1], depth, tabattachment=None, angle=0)

    def flip(self):
        """
        Flips all faces in graph
        """
        for f in self.faces:
            f.flip()

    def transform(self, scale=1, angle=0, origin=(0,0)):
      pass

    def dotransform(self, scale=1, angle=0, origin=(0,0)):
      for f in self.faces:
        f.transform(scale, angle, origin)

    def mirror_y(self):
      return
      for f in self.faces:
        f.transform( mirrorY())

    def mirror_x(self):
      return
      for f in self.faces:
        f.transform( mirrorX())

    def print_graph(self):
      """
      Prints all faces and edges in graph
      """
      print
      for f in self.faces:
        print f.name + repr(f.edges)

    def graph_obj(self):
      """
      Converts to an adjacency list graph representation

      Returns:
          dictionary that represents the adjacency list

      """
      g = {}
      for f in self.faces:
        g[f.name] = dict([(e and e.name or "", e) for e in f.edges])
      return g

    def show_graph(self):
      """
      Displays the graph as a vertex-edge graph
      """
      import objgraph
      objgraph.show_refs(self.graph_obj(), max_depth = 2, filter = lambda x : isinstance(x, (dict, HyperEdge)))

    def place(self, force=False):
      """
      Places all of the faces in the graph
      
      Args:
          force: whether to unplace first or not
      """
      if force:
          self.unplace()
      transform_2d = np.eye(4)
      transform_3d = np.eye(4)
      self.faces[0].place(None, transform_2d, transform_3d)

    def get_3d_com(self):
      """
      Calculates and returns the 3D center of mass
      
      Returns:
          the mass and center of mass
      """
      mass = 0
      com = np.zeros(3,1)
      for f in self.faces:
        mass += f.area
        com += f.get_3d_com()
      return mass, com/mass

    def unplace(self):
      """
      Unplaces all the faces and edges in the graph
      """
      for f in self.faces:
          f.transform2D = None
          f.transform3D = None

      for e in self.edges:
          f.pts2D = None
          f.pts3D = None

    def to_stl(self, filename):
      """
      Converts the graph to STL
      
      Args:
          filename (str): name of file to write STL data to
      """
      self.place()
      stlFaces = []
      for face in self.faces:
        if self.component.evalEquation(face.area) > 0:
          tdict = copy.deepcopy(face.getTriangleDict(self.component))
          newverts = []
          for vert in tdict["vertices"]:
            newverts.append(tuple(self.component.evalEquation(i) for i in vert))
          tdict["vertices"] = newverts
          stlFaces.append([self.component.evalEquation(face.transform3D), tdict, face.name])
        '''
        else:
          print "skipping face:", face.name
        '''
      stl_write(stlFaces, filename)

    def to_svg(self, filename):
      """
      Converts the graph to an SVG
      
      Args:
          filename (str): name of file to write SVG data to
      """
      # XXX TODO
      self.place()
      dxf_edges = [list(e.pts_2d) + [e.get_interior_angle()] for e in self.edges if e.pts_2d is not None]
      dxf_write(dxf_edges, filename)

    def to_dxf(self, filename):
      """
      Converts the graph to an SVG
      
      Args:
          filename (str): name of file to write SVG data to
      """
      self.place()
      dxf_edges = [list(e.pts_2d) + [e.get_interior_angle()] for e in self.edges if e.pts_2d is not None]
      dxf_write(dxf_edges, filename)
