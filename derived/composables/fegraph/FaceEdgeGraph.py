"""
Contains the Graph class and several helper functions.
"""

class FaceEdgeGraph():
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