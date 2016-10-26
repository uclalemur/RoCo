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