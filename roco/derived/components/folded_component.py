"""The FoldedComponent class.

This module contains the FoldedComponent class which is a base class
for all physical objects that can be constructed by folding 2D faces.

"""

from mechanical_component import MechanicalComponent
from roco.derived.composables.graph_composable import GraphComposable

class FoldedComponent(MechanicalComponent):
    """A type of MechanicalComponent is a base for all foldable structures.

    The FoldedComponent class contains a graph composable that stores the
    folded structure as the component is built.

    """

    def __init__(self, yaml_file=None, **kwargs):
        """ Initializes a FoldedComponent object

        Args:
            yaml_file (str): optional yaml file to load information from
        
        """
        self.GRAPH = 'graph'
        self.drawing = None
        MechanicalComponent.__init__(self, yaml_file, **kwargs)

    def define(self, origin=False, euler=False, quat=False, **kwargs):
        """Function that defines the state of a FoldedComponent

        Args:
            origin (bool): whether component starts at the origin or not
            euler (bool): whether to use euler angles to represent rotation or not
            quat (bool): whether to use quaternions to represent rotation or not
            **kwargs (dict): arbitrary keyword arguments for define
        """
        MechanicalComponent.define(self, origin, euler, quat, **kwargs)
        g = GraphComposable(transform = self.transform3D)
        self.composables[self.GRAPH] = g
        
        self.place = self.composables[self.GRAPH].place
        self.merge_edge = self.composables[self.GRAPH].merge_edge
        self.add_tab = self.composables[self.GRAPH].add_tab
        self.get_edge = self.composables[self.GRAPH].get_edge
        self.attach_face = self.composables[self.GRAPH].attach_face
        self.add_face = self.composables[self.GRAPH].add_face

if __name__ == "__main__":
    pass
    