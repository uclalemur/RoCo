"""Component class and helper function.

This module contains the Component class, as well as a helper function to load
components.

"""

from Parameterized import Parameterized

def getSubcomponentObject(component, name=None, **kwargs):
    """Function to generate an instantiated component from the class name.

    Args:
        component (str): The name of the component class to instantiate.
        name (:obj:`str`, optional): The name to set for the component.
        **kwargs: Arbitrary keyword arguments to pass into the constructor.

    Returns:
        The instantiated component.

    """


class Component(Parameterized):
    """The base class that all components derive from.

    A component is an abstract representation of an element of a device.

    Attributes:
        subcomponents (dict): dictionary of component objects that make up the
            overall component where the key is the name.
        connections (list): list of connection definitions from an interface
            to another interface with arguments associated.
        interfaces (dict): dictionary of interfaces where the key is the name
        composables (OrderedDict): an ordered dictionary of composables that
            define the output of the component.

    """
