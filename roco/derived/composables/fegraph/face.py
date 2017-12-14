"""The Face module.

This module contains the Face class, meant to be used with the Face-Edge Graph,
as well as several derived classes of Face, meant to provide convenient
definitions for commonly used geometries
"""

from hyper_edge import *
from roco.utils.transforms import *
from roco.utils.utils import prefix as prefix_string
import roco.utils.mymath as np
import roco.derived.composables.fegraph.drawing_edge as DE
import sympy
import math

NON_PARAM_LEN = 1

class Face(object):
    """Surface with a boundary defined by an ordered set of points.

    Faces are defined by a collection of points ordered according to the right
    hand rule, with the area defined in the x cross y direction, and Hyperedges
    connection consecutive points. Faces are meant to be used as part of the
    Graph class.

    Attributes:
        name (str): User given name to differentiate face
        edges (list): List of Hyperedges defining the boundary of the face
        decorations (list):
        transform2D (Matrix): Transformation matrix to translate the face to
            its position in 2D space
        transfrom3D (Matrix): Transformation matrix to translate the face to
            its position in 3D space
        pts_2D (list): List of tuples of doubles representing the points that
            make up the boundary of the face on the 2D plane
        pts_4D (Matrix): Matrix of points as homogeneous coordinates to allow
            for translations
        com_2D (tuple): Reference point for the Face???
        com_4D (Matrix): Homogeneous coordinates for com2D
        area (double): Area of the face

    """

    def __init__(self, name, pts, lens=[1], edge_names=True, edge_angles=None, edge_flips=None, all_edges=None,
                 decorations=None, recenter=False):
        """Initializes a Face object

        Args:
            name (str): name to give the Face
            pts (list): list of tuples that represent the points that make
                up the Face in 2D space.
            lens (list): list of lengths that represent the lengths of each
                side of the Face.
            edge_names (bool): whether to name the edges or not.
            edge_angles (list): list of angles between edges
            all_edges (list): list of all edges that make up Face
            decorations (list): list of decorations on Face
            recenter (bool): whether to recenter the Face or not

        """
        if len(pts) > len(lens):
            if len(lens) is 1:
                lens = lens * len(pts)
            else:
                raise Exception("The number of side lengths and the number of pts do not match!")
        if name:
            self.name = name
        else:
            self.name = ""
        self.lens = lens
        self.recenter(list(pts), recenter=recenter)

        self.edges = [None] * len(pts)
        if edge_names is True:
            edge_names = ["e%d" % i for i in range(len(pts))]
        self.rename_edges(edge_names, edge_angles, edge_flips, all_edges)

        if decorations:
            self.decorations = decorations
        else:
            self.decorations = []

        self.transform_2D = None
        self.transform_3D = None

    def recenter(self, pts, recenter=False):
        """Calculates the center of mass and moves CoM to origin if recenter is True

        Args:
            pts (list): list of tuples that represent the points that make up the Face in 2D space.
            recenter (bool): whether to move the center of mass to origin or not.

        """
        self.pts_2D = [(p[0], p[1]) for p in pts]

        # Put centroid of polygon at origin
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]

        a, cx, cy = 0, 0, 0
        for i in range(len(pts)):
            a += (xs[i] * ys[i + 1] - xs[i + 1] * ys[i]) / 2
            cx += (xs[i] + xs[i + 1]) * (xs[i] * ys[i + 1] - xs[i + 1] * ys[i]) / 6
            cy += (ys[i] + ys[i + 1]) * (xs[i] * ys[i + 1] - xs[i + 1] * ys[i]) / 6

        self.area = a

        if a == 0:
            self.pts_2D = [(p[0], p[1]) for p in pts]
            self.com_2D = (0, 0)
        else:
            if recenter:
                self.pts_2D = [(p[0] - cx / a, p[1] - cy / a) for p in pts]
                self.com_2D = (0, 0)
            else:
                self.pts_2D = [(p[0], p[1]) for p in pts]
                self.com_2D = (cx / a, cy / a)

        self.pts_4D = np.transpose(np.array([list(x) + [0, 1] for x in self.pts_2D]))
        self.com_4D = np.array(list(self.com_2D) + [0, 1])

    def rename(self, name):
        """Changes the name of this Face

        Args:
            name (str): name to change to.

        """
        self.name = name

    def prefix(self, prefix):
        """Prefixes the name and all the edge names of this Face

        Args:
            prefix (str): prefix to add to names of edges and itself.

        """
        self.name = prefix_string(prefix, self.name)
        self.prefix_edges(prefix)

    def prefix_edges(self, prefix):
        """Prefixes all edges contained by this Face

        Args:
            prefix (str): prefix to add to edge names

        """
        for e in self.edges:
            e.rename(prefix_string(prefix, e.name))

    def rename_edges(self, edge_names=None, edge_angles=None, edge_flips=None, all_edges=None):
        """Renames edges given by edge_names and sets their angle, flip and list of edges they're connected to.

        Args:
            edge_names (list): list of tuples (edge_index, new_name) where edge_index is the index to modify and
                               new_name is the name to rename the edge to.
            edge_angles (list): list of angles to set the edges at.
            edge_flips (list): list of booleans indicated whether to flip the edge in its connections or not.
            all_edges(list): list of edges that the edges in the Face should be connected to.

        Returns:
            This Face object

        """
        if edge_names:
            if edge_angles is None:
                edge_angles = [0] * len(edge_names)
            if edge_flips is None:
                edge_flips = [False] * len(edge_names)
            for (index, name) in enumerate(edge_names):
                self.set_edge(index, name, edge_angles[index], edge_flips[index], all_edges)
        return self

    def set_edge(self, index, name=None, angle=None, flip=False, all_edges=None):
        """Modifies the state of the edge at the given index

        Args:
            index (number): index of edge to modify
            name (str): name to give the edge
            angle (number): angle to set the edge to
            flip (bool): whether to flip the edge in connections or not
            all_edges (list): list of edges to connect the specified edge to

        Returns:
            This Face object

        """
        if name is None:
            return self
        try:
            if self.edges[index].name == name:
                if angle is not None:
                    self.edges[index].set_angle(angle, flip)
                return self
        except:
            pass

        self.disconnect(index)

        e = HyperEdge.edge(all_edges, name, length=self.edge_length(index), face=self, angle=angle, flip=flip)
        self.edges[index] = e

        return self

    def replace_edge(self, old_edge, new_edge, angle, flip):
        """Replaces old_edge with new_edge

        Args:
            old_edge (HyperEdge): edge to replace
            new_edge (HyperEdge): edge to replace with
            angle (number): angle edge is oriented at.
            flip (bool): whether connections on this edge flip faces or not.

        Returns:
            This Face object

        """
        for (i, e) in enumerate(self.edges):
            if e is old_edge:
                self.disconnect(i)
                self.edges[i] = new_edge
                new_edge.join(self.edge_length(i), self, angle=angle, flip=flip)
        return self

    def edge_index(self, name):
        """Returns the index of the edge given by the name

        Args:
            name (str): name of edge to find

        Returns:
            index of the edge with given name
        """
        for (i, e) in enumerate(self.edges):
            if name == e.name:
                return i

    def edge_coords(self, index):
        """Returns the coordinates of edge given by index

        Args:
            index (number): index of edge to return coordinates of.

        Returns:
            tuple of coordinates for the edge

        """
        return (self.pts_2D[index - 1], self.pts_2D[index])

    def edge_length(self, edge_index):
        """Returns the length of the edge given by the index
        """
        return self.lens[edge_index]

    def rotate(self, n=1):
        """Rotates the edges n times

        Args:
            n (number): number of times to rotate edges

        Returns:
            this Face object

        """
        for i in range(n):
            self.edges.append(self.edges.pop(0))
            self.pts_2D.append(self.pts_2D.pop(0))

        return self

    def flip(self):
        """Flips all the connections of the edges of this Face

        Args:
            None

        Returns:
            this Face object
        """
        new_edges = []
        new_pts = []
        while self.edges:
            new_edges.append(self.edges.pop())
            new_edges[-1].flip_connection(self)
            new_pts.append(self.pts_2D.pop())
        new_edges.insert(0, new_edges.pop())
        self.edges = new_edges
        self.pts_2D = new_pts
        return self

    def transform(self, scale=1, angle=0, origin=(0, 0)):
        r = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]]) * scale
        o = np.array([origin] * len(self.pts_2D))

        pts = np.transpose(np.dot(r, np.transpose(np.array(self.pts_2D)))) + o
        self.pts_2D = [tuple(x) for x in np.rows(pts)]
        for (i, d) in enumerate(self.decorations):
            o = np.array([origin] * len(d[0]))
            pts = np.transpose(np.dot(r, np.transpose(np.array(d[0])))) + o
            self.decorations[i] = ([tuple(x) for x in np.rows(pts)], d[1])

    def disconnect_from(self, edgename):
        for (i, e) in enumerate(self.edges):
            if edgename == e.name:
                return self.disconnect(i)
        return self

    def disconnect_all(self):
        for i in range(len(self.edges)):
            self.disconnect(i)
        return self

    def disconnect(self, index):
        e = self.edges[index]

        if e is None:
            return self

        self.edges[index] = None
        e.remove(self)
        return self

    def all_neighbors(self):
        n = []
        for es in self.neighbors():
            n.extend(es)
        return n

    def neighbors(self):
        n = []
        for e in self.edges:
            if e is None:
                n.append([])
            else:
                n.append([f.name for f in e.faces if f.name != self.name])
        return n

    def copy(self, name):
        return Face(name, self.pts_2D, decorations=self.decorations, recenter=False)

    def matches(self, other):
        if len(self.pts_2D) != len(other.pts_2D):
            return False
        # XXX TODO: verify congruence
        bothpts = zip(self.pts_2D, other.pts_2D)
        return True

    def add_decoration(self, pts):
        self.decorations.append(pts)

    def pre_transform(self, edge):
        index = self.edges.index(edge)
        # print edge
        # print self.edgeCoords(index)
        return np.dot(rotate_onto_x(*self.edge_coords(index)), move_to_origin(self.pts_2D[index]))

    def place(self, edge_from, transform_2D, transform_3D, placed=None):
        if self.transform_2D is not None and self.transform_3D is not None and placed is not None and self in \
                placed['faces']:
            # TODO : verify that it connects appropriately along alternate path
            # print "Repeated face : " + self.name
            return

        if placed is None:  # Replacing the entire component
            placed = {'faces': []}  ## create a dictionary: placed, the key is 'faces'.

        ## Face is being placed into the list of key:'faces'. placed={'faces':[face1,face2,...,facen]} ##
        placed['faces'].append(self)

        if edge_from is not None:
            r = self.pre_transform(edge_from)
        else:
            r = np.eye(4)   ## create a identity unit matrix. ##

        self.transform_2D = np.dot(transform_2D, r)
        self.transform_3D = np.dot(transform_3D, r)

        pts_2D = np.dot(r, self.pts_4D)[0:2, :]  ##using numpy, 0-2 rows and all columns. ##

        coords_2D = self.get_2D_coords()
        coords_3D = self.get_3D_coords()

        for (i, e) in enumerate(self.edges):
            # XXX hack: don't follow small edges
            if e is None or e.is_tab():  ## do nothing to edges which is tabbed or without connection? ##
                continue

            el = self.edge_length(i)  ##return the length of edge by edge index i. ##
            try:
                if el <= 0.01:
                    continue
            except TypeError:
                # print 'sympyicized variable detected - ignoring edge length check'
                pass

            da = e.faces[self]  ## e is an edge? ##
            if da[1]:
                e.place((coords_2D[:, i - 1], coords_2D[:, i]), (coords_3D[:, i - 1], coords_3D[:, i]))
            else:
                e.place((coords_2D[:, i], coords_2D[:, i - 1]), (coords_3D[:, i], coords_3D[:, i - 1]))

            if len(e.faces) <= 1:  ## how !!!!! ##
                # No other faces to be found, move on to next edge.
                continue

            pt1 = pts_2D[:, i - 1]
            pt2 = pts_2D[:, i]

            # TODO : Only skip self and the face that you came from to verify multi-connected edges
            # XXX : Assumes both faces have opposite edge orientation
            #       Only works for non-hyper edges -- need to store edge orientation info for a +/- da
            for (f, a) in e.faces.iteritems():
                if a[1] ^ da[1]:
                    # opposite orientation
                    pta, ptb = pt1, pt2
                else:
                    # same orientation
                    pta, ptb = pt2, pt1

                x = rotate_x_to(ptb, pta)

                r2d = np.eye(4)
                r2d = np.dot(x, r2d)
                r2d = np.dot(move_origin_to(pta), r2d)

                r3d = rotate_x(np.deg2rad(a[0] + da[0]))
                r3d = np.dot(x, r3d)
                r3d = np.dot(move_origin_to(pta), r3d)

                f.place(e, np.dot(transform_2D, r2d), np.dot(transform_3D, r3d), placed=placed)

    def get_triangle_dict(self, separateHoles=True):
        # print self.pts2d
        # if len(self.pts2d > 0):
        #  print type(self.pts2d[0])
        vertices = self.pts_2D

        segments = [(i, (i + 1) % len(vertices)) for i in range(len(vertices))]

        holes = []
        hole_vertices = []
        hole_segments = []
        for d in (x[0] for x in self.decorations if x[1] == "hole"):
            ld = len(d)
            if separateHoles:
                lv = len(hole_vertices)
                hole_vertices.append(d)
                hole_segments.extend([(lv + ((i + 1) % ld), lv + i) for i in range(ld)])
            else:
                lv = len(vertices)
                vertices.extend(d)
                segments.extend([(lv + ((i + 1) % ld), lv + i) for i in range(ld)])
            holes.append(tuple(np.sum([np.array(x) for x in d]) / len(d)))

        if hole_vertices:
            return dict(vertices=(vertices), segments=(segments),hole_vertices=(hole_vertices),hole_segments=(hole_segments), holes=(holes))
        if holes:
            return dict(vertices=(vertices), segments=(segments), holes=(holes))
        else:
            return dict(vertices=(vertices), segments=(segments))

    def get_2D_coords(self):
        if self.transform_2D is not None:
            return np.dot(self.transform_2D, self.pts_4D)[0:2, :]

    def get_2D_com(self):
        if self.transform_2D is not None:
            return np.dot(self.transform_2D, self.com_4D)[0:2, :]

    def get_2D_decorations(self):
        if self.transform_2D is not None:
            edges = []
            for i, e in enumerate(self.decorations):
                if e[1] == "hole":
                    for j in range(len(e[0])):
                        name = self.name + ".d%d.e%d" % (i, j)
                        pt1 = np.dot(self.transform_2D, np.array(list(e[0][j - 1]) + [0, 1]))[0:2]
                        pt2 = np.dot(self.transform_2D, np.array(list(e[0][j]) + [0, 1]))[0:2]
                        # XXX use EdgeType appropriately
                        edges.append([name, pt1, pt2, 1])
                else:
                    name = self.name + ".d%d" % i
                    pt1 = np.dot(self.transform_2D, np.array(list(e[0][0]) + [0, 1]))[0:2]
                    pt2 = np.dot(self.transform_2D, np.array(list(e[0][1]) + [0, 1]))[0:2]
                    edges.append([name, pt1, pt2, e[1]])
            return edges
        return []

    def get_3D_coords(self):
        if self.transform_3D is not None:
            return np.dot(self.transform_3D, self.pts_4D)[0:3, :]

    def get_3D_com(self):
        if self.transform_3D is not None:
            return np.dot(self.transform_3D, self.com_4D)[0:3, :]

    def get_3D_normal(self):
        if self.transform_3D is not None:
            o = np.dot(self.transform_3D, np.array([0, 0, 0, 1]))
            z = np.dot(self.transform_3D, np.array([0, 0, 1, 1]))
            return (z - o)[0:3, :]

    def __eq__(self, other):
        return self.name == other.name

    def get_6DOF(self):
        if self.transform_3D is not None:
            return get_6DOF(self.transform_3D)
        else:
            return get_6DOF(np.eye(4))

class RegularNGon(Face):
    """Subclass of Face representing regular polygons defined by side length
    """
    def __init__(self, name, n, length, edge_names=True, all_edges=None):
        pts = []
        lens = []
        radius = (length / (2 * np.sin(np.pi / n)))
        dt = (2 * np.pi / n)
        for i in range(n):
            pts.append((radius * np.cos(i * dt), radius * np.sin(i * dt)))
            lens.append(length)

        Face.__init__(self, name, pts, lens, edge_names=edge_names, allEdges=all_edges)

class RegularNGon2(Face):
    """Subclass of Face representing regular polygons defined by radius
    """
    def __init__(self, name, n, radius, edge_names=True, all_edges=None):
        pts = []
        lens = []
        dt = (2 * np.pi / n)
        for i in range(n):
            pts.append((radius * np.cos(i * dt), radius * np.sin(i * dt)))
            lens.append(0)
        Face.__init__(self, name, pts, lens, edge_names=edge_names, all_edges=all_edges)

class Square(RegularNGon):
    """Regular NGon with 4 sides
    """

    def __init__(self, name, length, edge_names=True, all_edges=None):
        RegularNGon.__init__(self, name, 4, length, edge_names=edge_names, all_edges=all_edges)

class Rectangle(Face):
    """Subclass of Face representing a quadrilateral with 4 right angles
    """

    def __init__(self, name, l, w, edge_names=True, all_edges=None, recenter=True):
        Face.__init__(self, name, ((l, 0), (l, w), (0, w), (0, 0)), [l, w, l, w], edge_names=edge_names,
                      all_edges = all_edges, recenter = recenter)

class RightTriangle(Face):
    """Subclass of Face representing a right triangle
    """

    def __init__(self, name, l, w, edge_names=True, all_edges=None):
        Face.__init__(self, name, ((l, 0), (0, w), (0, 0)), [l, sympy.sqrt(l ** 2 + w ** 2), w], edge_names = edge_names,
                      all_edges = all_edges)

class Triangle(Face):
    """Subclass of Face with three sides
    """

    def __init__(self, name, a, b, c, edge_names=True, all_edges=None, recenter=True):
        is_sympy = False
        try:
            if (a > (b + c)) or (b > (a + c)) or (c > (a + b)):
                raise ArithmeticError("Side lengths do not make a triangle")
        except TypeError:
            # print 'Sympyicized variable detected - ignoring edge length check'
            is_sympy = True

            pt1 = (0, 0)
            pt2 = (a, 0)
            cosC = ((a ** 2) + (b ** 2) - (c ** 2)) / (2.0 * a * b)
            pt3x = cosC * b
            if is_sympy:
                pt3y = b * sympy.sqrt(1 - (cosC ** 2))
            else:
                pt3y = b * math.sqrt(1 - (cosC ** 2))
            pt3 = (pt3x, pt3y)
            Face.__init__(self, name, (pt1, pt2, pt3), [b, a, c], edge_names=edge_names, all_edges=all_edges,
                          recenter=recenter)

class IsoscelesTriangle(Face):
  def __init__(self, name, base, height,edge_names=True, all_edges=None, recenter=True):
    pt1 = (0,0)
    pt2 = (base,0)
    pt3 =(base/2,height)
    Face.__init__(self,name,(pt1,pt2,pt3),[NON_PARAM_LEN,base,NON_PARAM_LEN], edge_names=edge_names,
                  all_edges=all_edges, recenter=recenter)
class Trapezoid(Face):
  def __init__(self, name, l1,l2, h, edge_names=True, all_edges=None, recenter=True):
    diff = (l1 - l2)/2
    pt1 = (0,0)
    pt2 = (l1,0)
    pt3 = (l1-diff,h)
    pt4 = (diff, h)
    Face.__init__(self, name, (pt1, pt2, pt3, pt4), [NON_PARAM_LEN, l1, NON_PARAM_LEN, l2], edge_names=edge_names,
                  all_edges=all_edges, recenter=recenter)

class Trapezoid2(Face):
  def __init__(self, name, l1,l2,l3, edge_names=True, all_edges=None, recenter=True):
    diff = (l1 - l2)/2
    h = sympy.sqrt((l3**2) - (diff**2))
    pt1 = (0,0)
    pt2 = (l1,0)
    pt3 = (l1-diff,h)
    pt4 = (diff, h)
    Face.__init__(self, name, (pt1, pt2, pt3, pt4), [l3, l1, l3, l2], edge_names=edge_names, all_edges=all_edges,
                  recenter=recenter)

class Pentagon(Face):
  def __init__(self, name, s, edge_names=True, all_edges=None, recenter=True):
    angle1 = np.pi*36/180
    angle2 = np.pi*54/180
    angle3 = np.pi*18/180
    pt1 = (0,0)
    pt2 = (s*np.cos(angle1), s*np.sin(angle1))
    pt3 = (2*s*np.cos(angle1), 0)
    pt4 = (2*s*np.cos(angle1)*np.sin(angle2), -1*2*s*np.cos(angle1)*np.cos(angle2))
    pt5 = (s*np.sin(angle3), -1*s*np.cos(angle3))
    Face.__init__(self, name, (pt1, pt2, pt3, pt4, pt5), [s, s, s, s, s], edge_names=edge_names, all_edges=all_edges,
                  recenter=recenter)
