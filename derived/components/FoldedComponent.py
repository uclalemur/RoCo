"""The FoldedComponent class.

This module contains the FoldedComponent class which is a base class
for all physical objects that can be constructed by folding 2D faces.

"""

class FoldedComponent(MechanicalComponent):
    """A type of MechanicalComponent is a base for all foldable structures.

    The FoldedComponent class contains a graph composable that stores the
    folded structure as the component is built.

    """
