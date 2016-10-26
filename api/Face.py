"""The Face module.

This module contains the Face class, meant to be used with the Face-Edge Graph,
as well as several derived classes of Face, meant to provide convenient
definitions for commonly used geometries
"""
class Face():
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
        pts2D (list): List of tuples of doubles representing the points that
            make up the boundary of the face on the 2D plane
        pts4D (Matrix): Matrix of points as homogeneous coordinates to allow
            for translations
        com2D (tuple): Reference point for the Face???
        com4D (Matrix): Homogeneous coordinates for com2D
        area (double): Area of the face


    """
class RegularNGon(Face):
    """Subclass of Face representing regular polygons defined by side length
    """

class RegularNGon2(Face):
    """Subclass of Face representing regular polygons defined by radius
    """

class Square(RegularNGon):
    """Regular NGon with 4 sides
    """

class Rectangle(Face):
    """Subclass of Face representing a quadrilateral with 4 right angles
    """

class RightTriangle(Face):
    """Subclass of Face representing a right triangle
    """

class Triangle(Face):
    """Subclass of Face with three sides
    """