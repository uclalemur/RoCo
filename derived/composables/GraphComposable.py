"""The GraphComposable Module

Contains the GraphComposable class, which adds output functionality to the
graph class
"""

from fegraph.FaceEdgeGraph import FaceEdgeGraph
from roco.api.Composable import Composable

class GraphComposable(Composable,FaceEdgeGraph):
    """Class allowing output to be produced from FaceEdgeGraphs

    The GraphComposable class adds the Composable interface to the
    FaceEdgeGraph class. With this class, graphs can be converted to drawings
    and output to a file or drawn using tkinter

    Attributes:
        component (FoldedComponent): Reference to the FoldedComponent
            represented by the graph
    """
